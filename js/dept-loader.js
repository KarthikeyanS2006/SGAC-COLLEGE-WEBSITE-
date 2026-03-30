// Department Page Dynamic Loader
// Include this script in department pages and call loadDeptData('deptKey')

function loadDeptData(deptKey) {
    const deptData = getDepartmentData(deptKey);
    if (!deptData) {
        console.log('No data found for department:', deptKey);
        return;
    }

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

    // Load Faculty tab
    const facultyContent = document.querySelector('#faculty .content-card');
    if (facultyContent && deptData.faculty && deptData.faculty.length > 0) {
        let facultyHtml = `
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
        `;
        
        deptData.faculty.forEach((f, index) => {
            facultyHtml += `
                <tr style="border-bottom: 1px solid var(--color-light-gray);">
                    <td style="padding: var(--space-md);">${index + 1}</td>
                    <td style="padding: var(--space-md);">${f.name}</td>
                    <td style="padding: var(--space-md);">${f.designation}</td>
                    <td style="padding: var(--space-md);">${f.qualification}</td>
                </tr>
            `;
        });
        
        facultyHtml += `
                    </tbody>
                </table>
            </div>
        `;
        facultyContent.innerHTML = facultyHtml;
    }

    // Load Activity tab
    const activityContent = document.querySelector('#activity .content-card');
    if (activityContent) {
        if (deptData.activities && deptData.activities.length > 0) {
            let activityHtml = '<h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">Department Activities</h3>';
            deptData.activities.forEach(activity => {
                activityHtml += `
                    <div style="padding: var(--space-md); border-left: 3px solid var(--color-gold); margin-bottom: var(--space-md); background: var(--color-light);">
                        <h4 style="color: var(--color-primary);">${activity.title}</h4>
                        <p style="color: var(--color-gray); font-size: 14px;">${activity.description}</p>
                    </div>
                `;
            });
            activityContent.innerHTML = activityHtml;
        } else {
            activityContent.innerHTML = `
                <h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">Department Activities</h3>
                <p style="text-align: center; color: var(--color-gray); padding: var(--space-3xl) 0;">
                    Activity details will be updated soon.
                </p>
            `;
        }
    }

    // Load Achievement tab
    const achievementContent = document.querySelector('#achievement .content-card');
    if (achievementContent) {
        if (deptData.achievements && deptData.achievements.length > 0) {
            let achievementHtml = '<h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">Department Achievements</h3>';
            deptData.achievements.forEach(achievement => {
                achievementHtml += `
                    <div style="padding: var(--space-md); border-left: 3px solid var(--color-gold); margin-bottom: var(--space-md); background: var(--color-light);">
                        <h4 style="color: var(--color-primary);">${achievement.title}</h4>
                        <p style="color: var(--color-gray); font-size: 14px;">${achievement.description}</p>
                    </div>
                `;
            });
            achievementContent.innerHTML = achievementHtml;
        } else {
            achievementContent.innerHTML = `
                <h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">Department Achievements</h3>
                <p style="text-align: center; color: var(--color-gray); padding: var(--space-3xl) 0;">
                    Achievement details will be updated soon.
                </p>
            `;
        }
    }

    // Load E-Content tab
    const econtentContent = document.querySelector('#econtent .content-card');
    if (econtentContent) {
        if (deptData.econtent && deptData.econtent.length > 0) {
            let econtentHtml = '<h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">E-Learning Resources</h3>';
            deptData.econtent.forEach(content => {
                econtentHtml += `
                    <div style="padding: var(--space-md); margin-bottom: var(--space-md); background: var(--color-light); border-radius: 8px;">
                        <h4 style="color: var(--color-primary);">${content.title}</h4>
                        <a href="${content.link}" style="color: var(--color-gold);">${content.link}</a>
                    </div>
                `;
            });
            econtentContent.innerHTML = econtentHtml;
        } else {
            econtentContent.innerHTML = `
                <h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">E-Learning Resources</h3>
                <p style="text-align: center; color: var(--color-gray); padding: var(--space-3xl) 0;">
                    E-content will be updated soon.
                </p>
            `;
        }
    }

    // Load Gallery tab
    const galleryContent = document.querySelector('#gallery .content-card');
    if (galleryContent) {
        if (deptData.gallery && deptData.gallery.length > 0) {
            let galleryHtml = '<h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">Department Gallery</h3><div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem;">';
            deptData.gallery.forEach(img => {
                galleryHtml += `<img src="${img}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px;">`;
            });
            galleryHtml += '</div>';
            galleryContent.innerHTML = galleryHtml;
        } else {
            galleryContent.innerHTML = `
                <h3 style="color: var(--color-primary); margin-bottom: var(--space-lg);">Department Gallery</h3>
                <p style="text-align: center; color: var(--color-gray); padding: var(--space-3xl) 0;">
                    Gallery images will be updated soon.
                </p>
            `;
        }
    }

    console.log('Department data loaded:', deptKey);
}
