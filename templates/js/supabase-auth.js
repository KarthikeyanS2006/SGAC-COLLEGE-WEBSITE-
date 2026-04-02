import { supabase } from './supabase-client.js';

let currentUser = null;
let authStateCallback = null;

export async function initAuth(callback) {
    authStateCallback = callback;
    const { data: { session } } = await supabase.auth.getSession();
    currentUser = session?.user || null;
    if (callback) callback(currentUser);
    supabase.auth.onAuthStateChange((event, session) => {
        currentUser = session?.user || null;
        if (callback) callback(currentUser);
    });
}

export async function signInWithMagicLink(email) {
    const { data, error } = await supabase.auth.signInWithOtp({
        email,
        options: {
            emailRedirectTo: window.location.origin + '/admin-supabase.html'
        }
    });
    return { data, error };
}

export async function signInWithPassword(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
    });
    return { data, error };
}

export async function signUp(email, password) {
    const { data, error } = await supabase.auth.admin.createUser({
        email,
        password,
        email_confirm: true
    });
    return { data, error };
}

export async function signOut() {
    const { error } = await supabase.auth.signOut();
    return { error };
}

export function getCurrentUser() {
    return currentUser;
}

export function isAuthenticated() {
    return currentUser !== null;
}
