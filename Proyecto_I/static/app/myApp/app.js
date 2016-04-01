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
            var bower = "../bower_components/material-design-icons/";
            $mdIconProvider
                .defaultIconSet("../img/svg/avatars.svg", 128)
                .icon("menu"       , "../img/svg/menu.svg"        , 24)
                .icon("contact"       , bower + "action/svg/design/ic_account_circle_24px.svg", 24)
                .icon("home"       , bower + "action/svg/design/ic_home_24px.svg", 24)
                .icon("group"       , bower + "social/svg/design/ic_group_24px.svg", 24)
                .icon("person"       , bower + "social/svg/design/ic_person_24px.svg", 24)
                .icon("email"      , bower + "communication/svg/design/ic_email_24px.svg", 24)
                .icon("google_plus", "../img/svg/google_plus.svg" , 512)
                .icon("hangouts"   , "../img/svg/hangouts.svg"    , 512)
                .icon("twitter"    , "../img/svg/twitter.svg"     , 512)
                .icon("phone"      , "../img/svg/phone.svg"       , 512);

            $mdThemingProvider.theme('default')
                .primaryPalette('blue')
                .accentPalette('light-blue');

        });

    app.run(runFn);

})());

