((function () {

    'use strict';

    function getStates() {
        return [
            {
                name: 'login',
                config: {
                    url: '/login',
                    templateUrl: 'app/myApp/auth/login/login.html',
                    controller: 'LoginCtrl'
                }
            },
            {
                name: 'signup',
                config: {
                    url: '/signup',
                    templateUrl: 'app/myApp/auth/signup/signup.html',
                    controller: 'SignupCtrl'
                }
            },
            {
                name: 'settings',
                config: {
                    url: '/settings',
                    templateUrl: 'app/myApp/auth/settings/settings.html',
                    controller: 'SettingsCtrl',
                    data: {
                        authenticate: true
                    }
                }
            }
        ];
    }

    /* @ngInject */
    function stateConfig(statehelper) {
        statehelper.configureStates(getStates());
    }

    angular
        .module('hiraApp.auth')
        .run(stateConfig);

})());
