// Dynamic Client-side Search Engine
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('catalogSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('#inventoryTable tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // Interactive safe disabling flow layout for submission pipelines
    const transactionForms = document.querySelectorAll('.action-form');
    transactionForms.forEach(form => {
        form.addEventListener('submit', () => {
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span> Processing...`;
            }
        });
    });

    // Smart UI Toggler for Dynamic Signup Field Setup Requirements
    const roleSelect = document.getElementById('id_role');
    const studentIdWrapper = document.getElementById('div_id_student_id');
    if (roleSelect && studentIdWrapper) {
        const toggleField = () => {
            studentIdWrapper.style.display = roleSelect.value === 'student' ? 'block' : 'none';
        };
        roleSelect.addEventListener('change', toggleField);
        toggleField();
    }
});