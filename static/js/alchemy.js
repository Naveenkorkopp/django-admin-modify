/* eslint-disable */
// Auto update layout
(function() {
  window.layoutHelpers.setAutoUpdate(true);
})();

// Collapse menu
(function() {
  if ($('#layout-sidenav').hasClass('sidenav-horizontal') || window.layoutHelpers.isSmallScreen()) {
    return;
  }

  try {
    window.layoutHelpers.setCollapsed(
      localStorage.getItem('layoutCollapsed') === 'true',
      false
    );
  } catch (e) {}
})();

$(function() {
  // Initialize sidenav
  $('#layout-sidenav').each(function() {
    new SideNav(this, {
      orientation: $(this).hasClass('sidenav-horizontal') ? 'horizontal' : 'vertical'
    });
  });

  // Initialize sidenav togglers
  $('body').on('click', '.layout-sidenav-toggle', function(e) {
    e.preventDefault();
    window.layoutHelpers.toggleCollapsed();
    if (!window.layoutHelpers.isSmallScreen()) {
      try { localStorage.setItem('layoutCollapsed', String(window.layoutHelpers.isCollapsed())); } catch (e) {}
    }
  });

  if ($('html').attr('dir') === 'rtl') {
    $('#layout-navbar .dropdown-menu').toggleClass('dropdown-menu-right');
  }
});

// LOGO SECTION MATCH HEIGHT OF BREADCRUMB
matchLogo();
$(window).on('resize', function() {
  // if($(window).outerWidth() <= 992) {
    matchLogo();
  // }
});

function matchLogo () {
  var crumbH = $('.layout-navbar').outerHeight();
  $('.app-brand').outerHeight(crumbH);

  //mobile toggle position
  $(`.navbar-collapse`).css({
    'top' : crumbH + 'px'
  });
}

// TRANSFER SEARCH BAR OBJECT TOOLS ELEMENTS TO SAME DIV
$(function() {
    // Don't apply this fix on the audit_core pages
    if ($('body').hasClass('app-audit_core')) {
      return;
    }

    // Reduce flicker
    $('.object-tools').css({'display': 'flex'});


    // Move .object-tools
    const getRow = document.querySelector(`.change-list .container-fluid .row`);

    if(getRow) {
      // create new container for search bar and object tools
      const newDiv = document.createElement(`div`);

      const toolBar = document.getElementById(`toolbar`);
      const objectTools = document.getElementById('content-main');

      getRow.insertBefore(newDiv, getRow.childNodes[0]);
      newDiv.setAttribute(`id`,`search-and-menu`);

      const newColumn = document.getElementById(`search-and-menu`);

      newColumn.classList.add(`col-lg-12`);

      // take nodes from original container and duplicate in new container.
      // elements in original containers automatically disappear
      if (toolBar) {
          newColumn.appendChild(toolBar.childNodes[0]);
          newColumn.classList.add('search-present');
      }
      objectTools && objectTools.childNodes[1].nodeName == `UL` ? newColumn.appendChild(objectTools.childNodes[1]) : ``;
    }

});
