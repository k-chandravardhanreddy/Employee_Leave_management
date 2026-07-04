/* ============================================================
   Employee Leave Management System — script.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Flash message auto-dismiss ─────────────────────── */
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(function (el) {
    // auto-remove after 4 s
    setTimeout(function () { dismissFlash(el); }, 4000);

    const btn = el.querySelector('.flash-close');
    if (btn) btn.addEventListener('click', function () { dismissFlash(el); });
  });

  function dismissFlash(el) {
    el.style.transition = 'opacity .3s, transform .3s';
    el.style.opacity = '0';
    el.style.transform = 'translateX(60px)';
    setTimeout(function () { el.remove(); }, 320);
  }

  /* ── Mobile sidebar toggle ───────────────────────────── */
  const mobileToggle  = document.getElementById('mobileToggle');
  const sidebar       = document.getElementById('sidebar');
  const sidebarBackdrop = document.getElementById('sidebarBackdrop');

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', openSidebar);
  }

  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener('click', closeSidebar);
  }

  function openSidebar() {
    sidebar.classList.add('open');
    sidebarBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  /* ── Active nav highlight ────────────────────────────── */
  const navItems = document.querySelectorAll('.nav-item');
  const currentPath = window.location.pathname;

  navItems.forEach(function (item) {
    if (item.getAttribute('href') === currentPath) {
      item.classList.add('active');
    }
  });

  /* ── Date validation for leave form ─────────────────── */
  const startDateInput = document.getElementById('start_date');
  const endDateInput   = document.getElementById('end_date');
  const totalDaysSpan  = document.getElementById('total_days_preview');

  if (startDateInput && endDateInput) {
    // Set minimum date as today
    const today = new Date().toISOString().split('T')[0];
    startDateInput.setAttribute('min', today);
    endDateInput.setAttribute('min', today);

    function updateTotalDays() {
      const s = new Date(startDateInput.value);
      const e = new Date(endDateInput.value);
      if (startDateInput.value && endDateInput.value) {
        if (e < s) {
          endDateInput.setCustomValidity('End date must be after start date.');
          if (totalDaysSpan) totalDaysSpan.textContent = '—';
        } else {
          endDateInput.setCustomValidity('');
          const diff = Math.floor((e - s) / (1000 * 60 * 60 * 24)) + 1;
          if (totalDaysSpan) {
            totalDaysSpan.textContent = diff + (diff === 1 ? ' day' : ' days');
          }
        }
      }
    }

    startDateInput.addEventListener('change', function () {
      endDateInput.setAttribute('min', this.value);
      updateTotalDays();
    });
    endDateInput.addEventListener('change', updateTotalDays);
  }

  /* ── Admin action modal ──────────────────────────────── */
  const actionModal   = document.getElementById('actionModal');
  const modalOverlay  = document.getElementById('modalOverlay');
  const modalTitle    = document.getElementById('modalTitle');
  const modalAction   = document.getElementById('modalAction');
  const modalLeaveId  = document.getElementById('modalLeaveId');
  const modalCloseBtn = document.querySelectorAll('.modal-close, #modalCancel');

  document.querySelectorAll('[data-action]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const action  = btn.dataset.action;
      const leaveId = btn.dataset.id;
      const empName = btn.dataset.name || '';

      if (modalTitle) {
        modalTitle.textContent = action + ' Leave Request';
      }
      if (modalAction)  modalAction.value  = action;
      if (modalLeaveId) modalLeaveId.value = leaveId;

      const descEl = document.getElementById('modalDesc');
      if (descEl) {
        descEl.textContent = action === 'Approved'
          ? `You are about to approve the leave request for ${empName}.`
          : `You are about to reject the leave request for ${empName}.`;
      }

      const confirmBtn = document.getElementById('modalConfirm');
      if (confirmBtn) {
        confirmBtn.className = 'btn ' + (action === 'Approved' ? 'btn-success' : 'btn-danger');
        confirmBtn.textContent = action === 'Approved' ? '✓ Approve' : '✗ Reject';
      }

      if (modalOverlay) modalOverlay.classList.add('active');
    });
  });

  modalCloseBtn.forEach(function (btn) {
    btn.addEventListener('click', closeModal);
  });

  if (modalOverlay) {
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) closeModal();
    });
  }

  function closeModal() {
    if (modalOverlay) modalOverlay.classList.remove('active');
  }

  /* ── Search with debounce ────────────────────────────── */
  const searchInput  = document.getElementById('searchInput');
  const filterStatus = document.getElementById('filterStatus');
  const filterDept   = document.getElementById('filterDept');

  function applyFilters() {
    const url = new URL(window.location.href);
    if (searchInput)  url.searchParams.set('search', searchInput.value);
    if (filterStatus) url.searchParams.set('status', filterStatus.value);
    if (filterDept)   url.searchParams.set('dept',   filterDept.value);
    window.location.href = url.toString();
  }

  let debounceTimer;
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(applyFilters, 600);
    });
  }
  if (filterStatus) filterStatus.addEventListener('change', applyFilters);
  if (filterDept)   filterDept.addEventListener('change', applyFilters);

  /* ── Balance progress bars ───────────────────────────── */
  document.querySelectorAll('.balance-fill[data-pct]').forEach(function (bar) {
    const pct = parseFloat(bar.dataset.pct) || 0;
    bar.style.width = Math.min(pct, 100) + '%';
  });

  /* ── Table row click → details ───────────────────────── */
  document.querySelectorAll('tr[data-href]').forEach(function (row) {
    row.style.cursor = 'pointer';
    row.addEventListener('click', function () {
      window.location.href = row.dataset.href;
    });
  });

  /* ── Confirm delete / logout prompt ─────────────────── */
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  /* ── Leave type badge colour on select change ────────── */
  const leaveTypeSelect = document.getElementById('leave_type');
  if (leaveTypeSelect) {
    function updateLeaveTypeBadge() {
      const preview = document.getElementById('leave_type_preview');
      if (!preview) return;
      preview.textContent = leaveTypeSelect.value || '';
      preview.className = 'badge badge-' + (leaveTypeSelect.value || '').toLowerCase();
    }
    leaveTypeSelect.addEventListener('change', updateLeaveTypeBadge);
    updateLeaveTypeBadge();
  }

  /* ── Animate stat numbers on dashboard ──────────────── */
  document.querySelectorAll('.stat-value[data-count]').forEach(function (el) {
    const target = parseInt(el.dataset.count, 10) || 0;
    let current  = 0;
    const step   = Math.ceil(target / 30);
    const timer  = setInterval(function () {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 30);
  });

});