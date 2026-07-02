// YTClone — Main JS

document.addEventListener('DOMContentLoaded', () => {

  // ── Sidebar toggle ──────────────────────────────────────────
  const toggleBtn = document.getElementById('sidebar-toggle');
  const sidebar   = document.getElementById('yt-sidebar');
  const main      = document.getElementById('yt-main');

  if (toggleBtn && sidebar && main) {
    // Restore saved state
    const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (collapsed) {
      sidebar.classList.add('collapsed');
      main.classList.add('sidebar-collapsed');
    }

    toggleBtn.addEventListener('click', () => {
      const isCollapsed = sidebar.classList.toggle('collapsed');
      main.classList.toggle('sidebar-collapsed', isCollapsed);
      localStorage.setItem('sidebarCollapsed', isCollapsed);
    });
  }

  // ── Auto-dismiss alerts ─────────────────────────────────────
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      const a = bootstrap.Alert.getOrCreateInstance(el);
      if (a) a.close();
    });
  }, 4000);

  // ── Shorts: auto-play first video ──────────────────────────
  const firstShort = document.querySelector('.yt-short-player-wrap video');
  if (firstShort) {
    firstShort.play().catch(() => {});
  }

  // ── Shorts: pause others when one plays ────────────────────
  document.querySelectorAll('.yt-short-player-wrap video').forEach(vid => {
    vid.addEventListener('play', () => {
      document.querySelectorAll('.yt-short-player-wrap video').forEach(other => {
        if (other !== vid) other.pause();
      });
    });
  });

  // ── Intersection Observer for Shorts auto-play ─────────────
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const video = entry.target.querySelector('video');
        if (!video) return;
        if (entry.isIntersecting) {
          video.play().catch(() => {});
        } else {
          video.pause();
        }
      });
    }, { threshold: 0.6 });

    document.querySelectorAll('.yt-short-item').forEach(item => {
      observer.observe(item);
    });
  }

  // ── Search bar — clear button & focus ──────────────────────
  const searchInput = document.querySelector('.yt-search-input');
  if (searchInput) {
    searchInput.addEventListener('focus', () => {
      searchInput.closest('.yt-search-wrap').style.borderColor = '#065fd4';
    });
    searchInput.addEventListener('blur', () => {
      searchInput.closest('.yt-search-wrap').style.borderColor = '#ccc';
    });
  }

  // ── Mobile sidebar overlay ─────────────────────────────────
  if (window.innerWidth < 900 && toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.remove('mobile-open');
      }
    });
  }

});

// ── Auth pages: password show/hide toggle ─────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.yt-pwd-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      const showing = input.type === 'text';
      input.type = showing ? 'password' : 'text';
      btn.innerHTML = showing ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
      btn.setAttribute('aria-label', showing ? btn.dataset.showLabel || 'Show password' : btn.dataset.hideLabel || 'Hide password');
    });
  });

  // ── Auth pages: live avatar preview on register ──────────────
  const avatarInput = document.getElementById('id_avatar');
  const avatarPreview = document.getElementById('avatarPreview');
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener('change', () => {
      const file = avatarInput.files && avatarInput.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        avatarPreview.innerHTML = `<img src="${e.target.result}" alt="">`;
      };
      reader.readAsDataURL(file);
    });
  }

  // ── Auth pages: password strength meter on register ──────────
  const pwd1 = document.getElementById('id_password1');
  const strengthWrap = document.getElementById('pwdStrengthWrap');
  const strengthFill = document.getElementById('pwdStrengthFill');
  const strengthLabel = document.getElementById('pwdStrengthLabel');
  if (pwd1 && strengthWrap && strengthFill && strengthLabel) {
    pwd1.addEventListener('input', () => {
      const val = pwd1.value;
      if (!val) { strengthWrap.style.visibility = 'hidden'; return; }
      strengthWrap.style.visibility = 'visible';
      let score = 0;
      if (val.length >= 8) score++;
      if (val.length >= 12) score++;
      if (/[a-z]/.test(val) && /[A-Z]/.test(val)) score++;
      if (/\d/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;
      const levels = [
        { pct: 20, color: '#cc0000', label: strengthWrap.dataset.labelWeak },
        { pct: 45, color: '#e8a200', label: strengthWrap.dataset.labelFair },
        { pct: 70, color: '#e8a200', label: strengthWrap.dataset.labelGood },
        { pct: 90, color: '#2ba640', label: strengthWrap.dataset.labelStrong },
        { pct: 100, color: '#2ba640', label: strengthWrap.dataset.labelStrong },
      ];
      const lvl = levels[Math.min(score, levels.length - 1)];
      strengthFill.style.width = lvl.pct + '%';
      strengthFill.style.background = lvl.color;
      strengthLabel.textContent = lvl.label;
      strengthLabel.style.color = lvl.color;
    });
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const wrap = document.getElementById('ytPlayer');
  if (!wrap) return;

  const video    = document.getElementById('ytVideo');
  const bigPlay  = document.getElementById('ytBigPlay');
  const clickEl  = document.getElementById('ytClickLayer');
  const playBtn  = document.getElementById('ytPlayBtn');
  const muteBtn  = document.getElementById('ytMuteBtn');
  const volume   = document.getElementById('ytVolume');
  const seek     = document.getElementById('ytSeek');
  const buffered = document.getElementById('ytBuffered');
  const timeEl   = document.getElementById('ytTime');
  const speed    = document.getElementById('ytSpeed');
  const fsBtn    = document.getElementById('ytFsBtn');
  const pipBtn   = document.getElementById('ytPipBtn');
  const ccBtn    = document.getElementById('ytCcBtn');
  const ccMenu   = document.getElementById('ytCcMenu');

  const PLAY  = '<i class="bi bi-play-fill"></i>';
  const PAUSE = '<i class="bi bi-pause-fill"></i>';

  function fmt(t) {
    if (!isFinite(t) || t < 0) return '0:00';
    t = Math.floor(t);
    const h = Math.floor(t / 3600);
    const m = Math.floor((t % 3600) / 60);
    const s = t % 60;
    const pad = n => String(n).padStart(2, '0');
    return h ? `${h}:${pad(m)}:${pad(s)}` : `${m}:${pad(s)}`;
  }

  function setFill(el) {
    const min = parseFloat(el.min) || 0;
    const max = parseFloat(el.max) || 100;
    const pct = ((parseFloat(el.value) - min) / (max - min)) * 100;
    el.style.setProperty('--pct', pct + '%');
  }

  // ── play / pause ──
  function togglePlay() {
    if (video.paused || video.ended) {
      video.play().catch(() => {});
    } else {
      video.pause();
    }
  }
  playBtn.addEventListener('click', togglePlay);
  bigPlay.addEventListener('click', togglePlay);
  clickEl.addEventListener('click', togglePlay);
  clickEl.addEventListener('dblclick', toggleFullscreen);

  video.addEventListener('play', () => {
    wrap.classList.add('playing');
    playBtn.innerHTML = PAUSE;
    showControls();
  });
  video.addEventListener('pause', () => {
    wrap.classList.remove('playing', 'inactive');
    playBtn.innerHTML = PLAY;
  });
  video.addEventListener('ended', () => {
    wrap.classList.remove('playing', 'inactive');
    playBtn.innerHTML = PLAY;
  });

  // ── buffering spinner ──
  video.addEventListener('waiting',  () => wrap.classList.add('buffering'));
  video.addEventListener('stalled',  () => wrap.classList.add('buffering'));
  video.addEventListener('playing',  () => wrap.classList.remove('buffering'));
  video.addEventListener('canplay',  () => wrap.classList.remove('buffering'));

  // ── time / seek ──
  video.addEventListener('loadedmetadata', () => {
    timeEl.textContent = `0:00 / ${fmt(video.duration)}`;
    setFill(seek);
  });
  video.addEventListener('timeupdate', () => {
    if (video.duration) {
      seek.value = (video.currentTime / video.duration) * 100;
      setFill(seek);
    }
    timeEl.textContent = `${fmt(video.currentTime)} / ${fmt(video.duration)}`;
  });
  seek.addEventListener('input', () => {
    if (video.duration) video.currentTime = (seek.value / 100) * video.duration;
    setFill(seek);
  });

  // ── buffered bar ──
  video.addEventListener('progress', () => {
    if (video.buffered.length && video.duration) {
      const end = video.buffered.end(video.buffered.length - 1);
      buffered.style.width = Math.min(100, (end / video.duration) * 100) + '%';
    }
  });

  // ── volume / mute ──
  video.volume = 1;
  volume.value = 1;
  setFill(volume);

  function updateVolIcon() {
    let icon = 'bi-volume-up-fill';
    if (video.muted || video.volume === 0)      icon = 'bi-volume-mute-fill';
    else if (video.volume < 0.5)                icon = 'bi-volume-down-fill';
    muteBtn.innerHTML = `<i class="bi ${icon}"></i>`;
  }
  volume.addEventListener('input', () => {
    video.volume = parseFloat(volume.value);
    video.muted  = (video.volume === 0);
    setFill(volume);
    updateVolIcon();
  });
  muteBtn.addEventListener('click', () => {
    video.muted = !video.muted;
    if (!video.muted && video.volume === 0) video.volume = 0.5;
    volume.value = video.muted ? 0 : video.volume;
    setFill(volume);
    updateVolIcon();
  });
  video.addEventListener('volumechange', () => {
    volume.value = video.muted ? 0 : video.volume;
    setFill(volume);
    updateVolIcon();
  });

  // ── playback speed ──
  speed.addEventListener('change', () => { video.playbackRate = parseFloat(speed.value); });

  // ── fullscreen ──
  function toggleFullscreen() {
    const fsEl = document.fullscreenElement || document.webkitFullscreenElement;
    if (!fsEl) {
      if (wrap.requestFullscreen)            wrap.requestFullscreen();
      else if (wrap.webkitRequestFullscreen) wrap.webkitRequestFullscreen();
      else if (video.webkitEnterFullscreen)  video.webkitEnterFullscreen(); // iOS Safari
    } else {
      if (document.exitFullscreen)            document.exitFullscreen();
      else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
    }
  }
  fsBtn.addEventListener('click', toggleFullscreen);

  function updateFsIcon() {
    const inFs = (document.fullscreenElement === wrap ||
                  document.webkitFullscreenElement === wrap);
    fsBtn.innerHTML = `<i class="bi ${inFs ? 'bi-fullscreen-exit' : 'bi-arrows-fullscreen'}"></i>`;
  }
  document.addEventListener('fullscreenchange', updateFsIcon);
  document.addEventListener('webkitfullscreenchange', updateFsIcon);

  // ── picture-in-picture ──
  if (pipBtn) {
    if (!('pictureInPictureEnabled' in document) || !document.pictureInPictureEnabled) {
      pipBtn.style.display = 'none';
    }
    pipBtn.addEventListener('click', async () => {
      try {
        if (document.pictureInPictureElement) await document.exitPictureInPicture();
        else await video.requestPictureInPicture();
      } catch (e) { /* ignore */ }
    });
  }

  // ── captions / subtitles (CC) ──
  let selectCaption = () => {};
  if (ccBtn && ccMenu) {
    const tracks = video.textTracks;
    const options = ccMenu.querySelectorAll('.yt-cc-option');

    // Never let the browser auto-show a track on load — we control visibility.
    for (let i = 0; i < tracks.length; i++) tracks[i].mode = 'hidden';

    selectCaption = (index) => {
      for (let i = 0; i < tracks.length; i++) {
        tracks[i].mode = (i === index) ? 'showing' : 'hidden';
      }
      options.forEach(opt => {
        opt.classList.toggle('active', parseInt(opt.dataset.index, 10) === index);
      });
      ccBtn.classList.toggle('active', index !== -1);
    };

    options.forEach(opt => {
      opt.addEventListener('click', (e) => {
        e.stopPropagation();
        selectCaption(parseInt(opt.dataset.index, 10));
        ccMenu.classList.remove('open');
      });
    });

    ccBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      ccMenu.classList.toggle('open');
    });
    ccMenu.addEventListener('click', (e) => e.stopPropagation());
    document.addEventListener('click', () => ccMenu.classList.remove('open'));
  }

  // ── auto-hide controls ──
  let hideTimer;
  function showControls() {
    wrap.classList.remove('inactive');
    clearTimeout(hideTimer);
    if (!video.paused) {
      hideTimer = setTimeout(() => wrap.classList.add('inactive'), 2600);
    }
  }
  wrap.addEventListener('mousemove', showControls);
  wrap.addEventListener('mouseleave', () => { if (!video.paused) wrap.classList.add('inactive'); });
  wrap.addEventListener('touchstart', showControls, { passive: true });

  // ── keyboard shortcuts ──
  document.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable) return;
    switch (e.key.toLowerCase()) {
      case ' ':
      case 'k': e.preventDefault(); togglePlay(); break;
      case 'f': toggleFullscreen(); break;
      case 'm': muteBtn.click(); break;
      case 'c':
        if (ccBtn) {
          const onIdx = ccMenu.querySelector('.yt-cc-option.active');
          if (onIdx) {
            selectCaption(-1);
          } else {
            const def = ccMenu.querySelector('.yt-cc-option[data-default="true"]') || ccMenu.querySelector('.yt-cc-option:not([data-index="-1"])');
            if (def) selectCaption(parseInt(def.dataset.index, 10));
          }
        }
        break;
      case 'arrowright': video.currentTime = Math.min(video.duration || 0, video.currentTime + 5); break;
      case 'arrowleft':  video.currentTime = Math.max(0, video.currentTime - 5); break;
      case 'arrowup':    e.preventDefault(); video.muted = false; video.volume = Math.min(1, video.volume + 0.1); break;
      case 'arrowdown':  e.preventDefault(); video.volume = Math.max(0, video.volume - 0.1); break;
      default: return;
    }
    showControls();
  });

  // ── init: try to autoplay WITH sound; if blocked, stay paused ──
  updateVolIcon();
  const attempt = video.play();
  if (attempt && typeof attempt.catch === 'function') {
    attempt.catch(() => {
      wrap.classList.remove('playing');
      playBtn.innerHTML = PLAY;   // user clicks play → plays with sound
    });
  }
});
