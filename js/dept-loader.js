// Department Page Dynamic Loader
// Include this script in department pages and call loadDeptData('deptKey')

async function loadDeptData(deptKey) {
    try {
        const apiBase = window.location.origin;
        
        const response = await fetch(`${apiBase}/api/public/all`);
        if (!response.ok) throw new Error('Failed to load departments');
        const data = await response.json();
        
        const dept = data.departments.find(d => d.dept_key === deptKey);
        if (!dept) {
            console.log('No data found for department:', deptKey);
            return;
        }

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

        // Update page title
        const titleEl = document.querySelector('.college-name, h1');
        if (titleEl && titleEl.textContent.includes('Department')) {
            titleEl.textContent = 'Department of ' + deptData.name;
        }

        // Update banner title
        const bannerTitle = document.querySelector('.content-section h1');
        if (bannerTitle) {
            bannerTitle.innerHTML = `<i class="fas ${deptData.icon || 'fa-book'}" style="margin-right: var(--space-md); color: var(--color-gold);"></i> Department of ${deptData.name}`;
        }

        // Load About tab
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

        // Load Vision/Mission tab
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

        console.log('Department data loaded:', deptKey);
    } catch (error) {
        console.error('Error loading department data:', error);
    }
}
