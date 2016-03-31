((function () {

    'use strict';

    var app = angular.module('hiraApp', [
        //hiraApp reusable features
        'hiraApp.core',
        //hiraApp data module
        'hiraApp.data',

        //hiraApp auth module
        'hiraApp.auth',

        //hiraApp DOM structure
        'hiraApp.layout',

        //hiraApp states
        'hiraApp.dashboard'
    ]);

    /*@ngInject*/
    function authInterceptor($q, $injector, authToken) {
        return {
            // Add authorization token to headers
            request: function (config) {
                config.headers = config.headers || {};

                //var authToken = $injector.get('authToken');
                var token = authToken.getToken();

                if (token) {
                    config.headers.Authorization = 'Bearer ' + token;
                }

                return config;
            },

            // Intercept 401s and redirect you to login
            responseError: function (response) {
                if (response.status === 401) {
                    $injector.get('$state').go('login');
                    // remove any stale tokens
                    authToken.removeToken();
                    return $q.reject(response);
                } else {
                    return $q.reject(response);
                }
            }
        };
    }

    app.factory('authInterceptor', authInterceptor);

    /*@ngInject*/
    function runFn(Auth, common) {
        var $state = common.$state;
        var $log = common.$log;
        var $rootScope = common.$rootScope;

        $log.info('Made with ♥ by IRB.IO\n\n-You want to work with us? Write a message to jobs@irb.io-');
        // Redirect to login if route requires auth and you're not logged in

        $rootScope.$on('$stateChangeStart', function (event, next) {
            Auth.isLoggedInAsync(function (loggedIn) {
                if (next.data && next.data.authenticate && !loggedIn) {
                    event.preventDefault();
                    $state.go('login');
                }
            });
        });
    }

    app.config(function($mdThemingProvider, $mdIconProvider){
            $mdIconProvider
                .defaultIconSet("./assets/images/svg/avatars.svg", 128)
                .icon("menu"       , "./assets/images/svg/menu.svg"        , 24)
                .icon("share"      , "./assets/images/svg/share.svg"       , 24)
                .icon("google_plus", "./assets/images/svg/google_plus.svg" , 512)
                .icon("hangouts"   , "./assets/images/svg/hangouts.svg"    , 512)
                .icon("twitter"    , "./assets/images/svg/twitter.svg"     , 512)
                .icon("phone"      , "./assets/images/svg/phone.svg"       , 512);

            $mdThemingProvider.theme('default')
                .primaryPalette('brown')
                .accentPalette('red');

        });

    app.run(runFn);

})());

