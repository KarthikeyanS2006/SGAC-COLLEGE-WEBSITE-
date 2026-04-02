import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

const SUPABASE_URL = 'https://fqdvvbgzbusqushsxzlyx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxZHd2YmdienVzcXVzaHN4emx4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5Njc1NzUsImV4cCI6MjA5MDU0MzU3NX0.C6Xs8eMSqd50ZSWa6YkhOpppdpF0A5aLDljffmF2rXU';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
export { SUPABASE_URL, SUPABASE_ANON_KEY };
