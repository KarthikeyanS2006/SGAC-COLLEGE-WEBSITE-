// Department Page Dynamic Loader
// Include this script in department pages and call loadDeptData('deptKey')

async function loadDeptData(deptKey) {
    try {
        const apiBase = window.location.origin;
        
        const response = await fetch(`${apiBase}/api/public/departments/${deptKey}`);
        if (!response.ok) {
            const allResp = await fetch(`${apiBase}/api/public/all`);
            const data = await allResp.json();
            const dept = data.departments.find(d => d.dept_key === deptKey);
            if (!dept) {
                console.log('No data found for department:', deptKey);
                return;
            }
            loadDeptBasicData(dept);
            return;
        }
        const dept = await response.json();
        
        loadDeptBasicData(dept);
        
        loadFacultyTab(dept.faculty || []);
        
        console.log('Department data loaded:', deptKey);
    } catch (error) {
        console.error('Error loading department data:', error);
    }
}

function loadDeptBasicData(dept) {
    const deptData = {
        name: dept.name,
        icon: dept.icon,
        about: dept.about,
        vision: dept.vision,
        mission: dept.mission,
        hod: {
            name: dept.hod_name,
            designation: dept.hod_designation,
            qualification: dept.hod_qualification,
            email: dept.hod_email,
            phone: dept.hod_phone
        }
    };

    const titleEl = document.querySelector('.college-name, h1');
    if (titleEl && titleEl.textContent.includes('Department')) {
        titleEl.textContent = 'Department of ' + deptData.name;
    }

    const bannerTitle = document.querySelector('.content-section h1');
    if (bannerTitle) {
        bannerTitle.innerHTML = `<i class="fas ${deptData.icon || 'fa-book'}" style="margin-right: var(--space-md); color: var(--color-gold);"></i> Department of ${deptData.name}`;
    }

    const aboutContent = document.querySelector('#about .content-card');
    if (aboutContent && deptData.about) {
        aboutContent.innerHTML = `
            <h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">
                <i class="fas fa-info-circle" style="color: var(--color-gold);"></i>
                About Our Department
            </h3>
            <p style="text-indent: 50px; text-align: justify; font-size: 17px; line-height: 1.8; margin-bottom: var(--space-md);">
                ${deptData.about}
            </p>
        `;
    }

    const visionContent = document.querySelector('#vision .content-card');
    if (visionContent) {
        visionContent.innerHTML = `
            <h4 style="color: var(--color-primary); margin-bottom: var(--space-md); font-size: var(--font-size-xl);">
                <i class="far fa-eye" style="color: var(--color-gold);"></i> Vision:
            </h4>
            <p style="font-size: 17px; line-height: 1.8; margin-bottom: var(--space-xl);">
                ${deptData.vision || 'Vision statement will be updated soon.'}
            </p>
            <h4 style="color: var(--color-primary); margin-bottom: var(--space-md); font-size: var(--font-size-xl);">
                <i class="fas fa-bullseye" style="color: var(--color-gold);"></i> Mission:
            </h4>
            <p style="font-size: 17px; line-height: 1.8;">
                ${deptData.mission || 'Mission statement will be updated soon.'}
            </p>
        `;
    }
}

function loadFacultyTab(faculty) {
    const facultyContent = document.querySelector('#faculty .content-card');
    if (!facultyContent) return;
    
    if (!faculty || faculty.length === 0) {
        facultyContent.innerHTML = `
            <div style="text-align: center; margin-bottom: var(--space-2xl);">
                <h2 style="color: var(--color-primary); margin-bottom: var(--space-md);">Our Faculty</h2>
                <p style="color: var(--color-gray); font-style: italic;">"Teaching is the one profession that creates all other professions"</p>
            </div>
            <p style="text-align: center; color: var(--color-gray);">Faculty information will be updated soon.</p>
        `;
        return;
    }
    
    const rows = faculty.map((f, i) => `
        <tr style="border-bottom: 1px solid var(--color-light-gray);">
            <td style="padding: var(--space-md);">${i + 1}</td>
            <td style="padding: var(--space-md);">${f.name}</td>
            <td style="padding: var(--space-md);">${f.designation || '-'}</td>
            <td style="padding: var(--space-md);">${f.qualification || '-'}</td>
        </tr>
    `).join('');
    
    facultyContent.innerHTML = `
        <div style="text-align: center; margin-bottom: var(--space-2xl);">
            <h2 style="color: var(--color-primary); margin-bottom: var(--space-md);">Our Faculty</h2>
            <p style="color: var(--color-gray); font-style: italic;">"Teaching is the one profession that creates all other professions"</p>
        </div>
        <div class="table-responsive">
            <table class="table" style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: var(--color-primary); color: var(--color-white);">
                        <th style="padding: var(--space-md); text-align: left;">S.No</th>
                        <th style="padding: var(--space-md); text-align: left;">Name</th>
                        <th style="padding: var(--space-md); text-align: left;">Designation</th>
                        <th style="padding: var(--space-md); text-align: left;">Qualification</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
    `;
}
