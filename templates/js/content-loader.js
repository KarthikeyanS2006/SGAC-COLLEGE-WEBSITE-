import { supabase } from './supabase-client.js';

export async function fetchNews() {
    const { data, error } = await supabase
        .from('news')
        .select('*')
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchEvents() {
    const { data, error } = await supabase
        .from('events')
        .select('*')
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchDownloads() {
    const { data, error } = await supabase
        .from('downloads')
        .select('*')
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchCarousel() {
    const { data, error } = await supabase
        .from('carousel')
        .select('*')
        .order('sort_order', { ascending: true });
    return { data: data || [], error };
}

export async function fetchAnnouncements() {
    const { data, error } = await supabase
        .from('announcements')
        .select('*')
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchDepartments() {
    const { data, error } = await supabase
        .from('departments')
        .select('*')
        .order('sort_order', { ascending: true });
    return { data: data || [], error };
}

export async function fetchDepartment(key) {
    const { data, error } = await supabase
        .from('departments')
        .select('*')
        .eq('dept_key', key)
        .single();
    return { data, error };
}

export async function fetchFaculty(deptId) {
    const { data, error } = await supabase
        .from('faculty')
        .select('*')
        .eq('department_id', deptId)
        .order('sort_order', { ascending: true });
    return { data: data || [], error };
}

export async function fetchGallery(deptId) {
    const { data, error } = await supabase
        .from('gallery')
        .select('*')
        .eq('department_id', deptId)
        .order('sort_order', { ascending: true });
    return { data: data || [], error };
}

export async function fetchActivities(deptId) {
    const { data, error } = await supabase
        .from('activities')
        .select('*')
        .eq('department_id', deptId)
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchAchievements(deptId) {
    const { data, error } = await supabase
        .from('achievements')
        .select('*')
        .eq('department_id', deptId)
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchEcontent(deptId) {
    const { data, error } = await supabase
        .from('econtent')
        .select('*')
        .eq('department_id', deptId)
        .order('created_at', { ascending: false });
    return { data: data || [], error };
}

export async function fetchSiteConfig() {
    const { data, error } = await supabase
        .from('site_config')
        .select('*')
        .single();
    return { data, error };
}

export async function fetchAllData() {
    const [newsRes, eventsRes, downloadsRes, carouselRes, announcementsRes, deptsRes] = await Promise.all([
        fetchNews(),
        fetchEvents(),
        fetchDownloads(),
        fetchCarousel(),
        fetchAnnouncements(),
        fetchDepartments()
    ]);
    return {
        news: newsRes.data,
        events: eventsRes.data,
        downloads: downloadsRes.data,
        carousel: carouselRes.data,
        announcements: announcementsRes.data,
        departments: deptsRes.data,
        errors: {
            news: newsRes.error,
            events: eventsRes.error,
            downloads: downloadsRes.error,
            carousel: carouselRes.error,
            announcements: announcementsRes.error,
            departments: deptsRes.error
        }
    };
}
