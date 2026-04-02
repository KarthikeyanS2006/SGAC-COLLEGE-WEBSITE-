import { supabase } from './supabase-client.js';

export async function saveNews(item) {
    const { data, error } = await supabase
        .from('news')
        .insert([{
            title: item.title,
            date: item.date || new Date().toISOString().split('T')[0],
            icon: item.icon || 'fa-bullhorn'
        }])
        .select()
        .single();
    return { data, error };
}

export async function updateNews(id, item) {
    const { data, error } = await supabase
        .from('news')
        .update({
            title: item.title,
            date: item.date,
            icon: item.icon
        })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteNews(id) {
    const { error } = await supabase
        .from('news')
        .delete()
        .eq('id', id);
    return { error };
}

export async function saveEvent(item) {
    const { data, error } = await supabase
        .from('events')
        .insert([{
            title: item.title,
            date: item.date || new Date().toISOString().split('T')[0],
            icon: item.icon || 'fa-calendar'
        }])
        .select()
        .single();
    return { data, error };
}

export async function updateEvent(id, item) {
    const { data, error } = await supabase
        .from('events')
        .update({
            title: item.title,
            date: item.date,
            icon: item.icon
        })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteEvent(id) {
    const { error } = await supabase
        .from('events')
        .delete()
        .eq('id', id);
    return { error };
}

export async function saveDownload(item) {
    const { data, error } = await supabase
        .from('downloads')
        .insert([{
            title: item.title,
            link: item.link,
            icon: item.icon || 'fa-download'
        }])
        .select()
        .single();
    return { data, error };
}

export async function updateDownload(id, item) {
    const { data, error } = await supabase
        .from('downloads')
        .update({
            title: item.title,
            link: item.link,
            icon: item.icon
        })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteDownload(id) {
    const { error } = await supabase
        .from('downloads')
        .delete()
        .eq('id', id);
    return { error };
}

export async function saveCarouselItem(item) {
    const { data: existing } = await supabase
        .from('carousel')
        .select('id, sort_order')
        .order('sort_order', { ascending: false })
        .limit(1);
    const nextOrder = existing && existing[0] ? existing[0].sort_order + 1 : 1;
    const { data, error } = await supabase
        .from('carousel')
        .insert([{
            img: item.img,
            alt: item.alt || '',
            sort_order: nextOrder
        }])
        .select()
        .single();
    return { data, error };
}

export async function updateCarouselItem(id, item) {
    const { data, error } = await supabase
        .from('carousel')
        .update({ img: item.img, alt: item.alt })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteCarouselItem(id) {
    const { error } = await supabase
        .from('carousel')
        .delete()
        .eq('id', id);
    return { error };
}

export async function saveAnnouncement(item) {
    const { data, error } = await supabase
        .from('announcements')
        .insert([{ text: item.text }])
        .select()
        .single();
    return { data, error };
}

export async function updateAnnouncement(id, item) {
    const { data, error } = await supabase
        .from('announcements')
        .update({ text: item.text })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteAnnouncement(id) {
    const { error } = await supabase
        .from('announcements')
        .delete()
        .eq('id', id);
    return { error };
}

export async function saveDepartment(item) {
    const { data: existing } = await supabase
        .from('departments')
        .select('id, sort_order')
        .order('sort_order', { ascending: false })
        .limit(1);
    const nextOrder = existing && existing[0] ? existing[0].sort_order + 1 : 1;
    const { data, error } = await supabase
        .from('departments')
        .insert([{
            dept_key: item.dept_key,
            name: item.name,
            icon: item.icon || 'fa-book',
            about: item.about || '',
            vision: item.vision || '',
            mission: item.mission || '',
            hod_name: item.hod_name || '',
            hod_designation: item.hod_designation || '',
            hod_qualification: item.hod_qualification || '',
            hod_email: item.hod_email || '',
            hod_phone: item.hod_phone || '',
            sort_order: nextOrder
        }])
        .select()
        .single();
    return { data, error };
}

export async function updateDepartment(id, item) {
    const { data, error } = await supabase
        .from('departments')
        .update({
            name: item.name,
            icon: item.icon,
            about: item.about,
            vision: item.vision,
            mission: item.mission,
            hod_name: item.hod_name,
            hod_designation: item.hod_designation,
            hod_qualification: item.hod_qualification,
            hod_email: item.hod_email,
            hod_phone: item.hod_phone
        })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteDepartment(id) {
    await supabase.from('faculty').delete().eq('department_id', id);
    await supabase.from('gallery').delete().eq('department_id', id);
    await supabase.from('activities').delete().eq('department_id', id);
    await supabase.from('achievements').delete().eq('department_id', id);
    await supabase.from('econtent').delete().eq('department_id', id);
    const { error } = await supabase.from('departments').delete().eq('id', id);
    return { error };
}

export async function saveFaculty(departmentId, item) {
    const { data: existing } = await supabase
        .from('faculty')
        .select('id, sort_order')
        .eq('department_id', departmentId)
        .order('sort_order', { ascending: false })
        .limit(1);
    const nextOrder = existing && existing[0] ? existing[0].sort_order + 1 : 1;
    const { data, error } = await supabase
        .from('faculty')
        .insert([{
            department_id: departmentId,
            name: item.name,
            designation: item.designation || '',
            qualification: item.qualification || '',
            email: item.email || '',
            phone: item.phone || '',
            sort_order: nextOrder
        }])
        .select()
        .single();
    return { data, error };
}

export async function updateFaculty(id, item) {
    const { data, error } = await supabase
        .from('faculty')
        .update({
            name: item.name,
            designation: item.designation,
            qualification: item.qualification,
            email: item.email,
            phone: item.phone
        })
        .eq('id', id)
        .select()
        .single();
    return { data, error };
}

export async function deleteFaculty(id) {
    const { error } = await supabase.from('faculty').delete().eq('id', id);
    return { error };
}

export async function saveGalleryItem(departmentId, item) {
    const { data: existing } = await supabase
        .from('gallery')
        .select('id, sort_order')
        .eq('department_id', departmentId)
        .order('sort_order', { ascending: false })
        .limit(1);
    const nextOrder = existing && existing[0] ? existing[0].sort_order + 1 : 1;
    const { data, error } = await supabase
        .from('gallery')
        .insert([{
            department_id: departmentId,
            src: item.src,
            caption: item.caption || '',
            sort_order: nextOrder
        }])
        .select()
        .single();
    return { data, error };
}

export async function deleteGalleryItem(id) {
    const { error } = await supabase.from('gallery').delete().eq('id', id);
    return { error };
}

export async function saveActivity(departmentId, item) {
    const { data, error } = await supabase
        .from('activities')
        .insert([{
            department_id: departmentId,
            title: item.title,
            description: item.description || '',
            date: item.date || new Date().toISOString().split('T')[0]
        }])
        .select()
        .single();
    return { data, error };
}

export async function deleteActivity(id) {
    const { error } = await supabase.from('activities').delete().eq('id', id);
    return { error };
}

export async function saveAchievement(departmentId, item) {
    const { data, error } = await supabase
        .from('achievements')
        .insert([{
            department_id: departmentId,
            title: item.title,
            description: item.description || '',
            student_name: item.student_name || ''
        }])
        .select()
        .single();
    return { data, error };
}

export async function deleteAchievement(id) {
    const { error } = await supabase.from('achievements').delete().eq('id', id);
    return { error };
}

export async function saveEcontent(departmentId, item) {
    const { data, error } = await supabase
        .from('econtent')
        .insert([{
            department_id: departmentId,
            title: item.title,
            link: item.link,
            description: item.description || ''
        }])
        .select()
        .single();
    return { data, error };
}

export async function deleteEcontent(id) {
    const { error } = await supabase.from('econtent').delete().eq('id', id);
    return { error };
}

export async function saveSiteConfig(item) {
    const { data, error } = await supabase
        .from('site_config')
        .upsert(item)
        .select()
        .single();
    return { data, error };
}
