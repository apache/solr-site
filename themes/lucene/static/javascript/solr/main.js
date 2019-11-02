;(function() {

  /*
   * --------------------------------------------------------------------------
   *  Initialize non-Angular components (limit this)
   * --------------------------------------------------------------------------
   */


  $(function() {
    $('h2').addClass('offset');
    $('.smooth-scroll').smoothScroll({ offset: 100 })
  });

  /*
   * Shrinking top-bar
   */
  $(function() {
    var header = $(".top-bar")
    $(window).scroll(function() {
      var scroll = $(window).scrollTop();
        if (scroll >= 150) {
            $(header).addClass("shrink");
        }
        if (scroll < 150) {
            $(header).removeClass("shrink");
        }
    });
  });

  angular.module('page', [])

    .controller('page.controllers.main', [
      '$scope',
      function($scope) {

        /*
         * Initialize.
         */

        /*
         * View methods.
         */
        $scope.select = function(key, n) {
          $scope.model[key] = n
        }

        $scope.isSelected = function(key, n) {
          return $scope.model[key] == n
        }

      }
    ])

    .directive('navigation', [function() {
      return {
        restrict: 'C',
        scope: true,
        link: function(scope, el, attrs) {

          scope.model = {
            path: ''
          }

          scope.$watch(function() { return window.location.pathname }, function(n, o, s) {
            scope.model.path = window.location.pathname
            $(el).find('a').removeClass('selected')
            $(el).find('a[href="' + scope.model.path + '"]').addClass('selected')
          })

        }
      }
    }])

    .directive('toggle', ['$window', function($window) {
      return {
        restrict: 'C',
        scope: true,
        link: function(scope, el, attrs) {

          var windowEl = angular.element($window),
            offset = el.offset().top,
            handler = function() {
              scope.scroll = windowEl.scrollTop()
            },
            focusSearch = function() {
              window.setTimeout(function() {
                $('input[type="search"]').focus()
              }, 1)
            }

          windowEl.on('scroll', scope.$apply.bind(scope, handler))
          handler();

          scope.toggled = false
          scope.toggle = function() {
            if(!scope.toggled && scope.scroll > 100) {
              $.smoothScroll({
                afterScroll: function() {
                  scope.$apply(function() {
                    scope.toggled = true
                    focusSearch()
                  })
                }
              }, 0)
            } else {
              scope.toggled = true
              focusSearch()
            }
          }

          scope.$watch('scroll', function(n, o, s) {
            if(n > 100) {
              scope.toggled = false
            }
            
          })

        }
      }

    }])

    .directive('anchorTop', ['$window', function($window) {
      return {
        restrict: 'C',
        scopr: true,
        link: function(scope, el, attrs) {

          var windowEl = angular.element($window),
            offset = el.offset().top,
            handler = function() {
              scope.scroll = windowEl.scrollTop()
            }

          windowEl.on('scroll', scope.$apply.bind(scope, handler))
          handler();

          scope.$watch('scroll', function(n, o, s) {
            var difference = (-1 * (offset - n)) + 57;
            if(difference > 0) {
              el.addClass('anchor-fixed')
            } else {
              el.removeClass('anchor-fixed')
            }
          })

        }
      }
    }])

})()
