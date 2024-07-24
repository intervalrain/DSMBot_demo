function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const resizer = document.getElementById('resizer');

    let isResizing = false;

    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    resizer.addEventListener('mousedown', (e) => {
        if (!sidebar.classList.contains('collapsed')) {
            isResizing = true;
            document.addEventListener('mousemove', resize);
            document.addEventListener('mouseup', stopResize);
        }
    });

    function resize(e) {
        if (isResizing && !sidebar.classList.contains('collapsed')) {
            const newWidth = e.clientX - sidebar.getBoundingClientRect().left;
            if (newWidth > 100 && newWidth < window.innerWidth * 0.5) {
                sidebar.style.width = newWidth + 'px';
            }
        }
    }

    function stopResize() {
        isResizing = false;
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
}