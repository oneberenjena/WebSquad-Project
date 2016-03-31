((function () {

    'use strict';

    /* @ngInject */
    function configure($stateProvider, $urlRouterProvider, $locationProvider,
            $httpProvider, statehelperConfigProvider, localStorageServiceProvider) {

        function configureRouting() {
            //HTML5 Mode and interceptors, CROSS Domain
            //$locationProvider.html5Mode(true);
            localStorageServiceProvider.setPrefix('ls.irbio.');
            $httpProvider.interceptors.push('authInterceptor');

            $httpProvider.defaults.useXDomain = true;
            delete $httpProvider.defaults.headers.common['X-Requested-With'];

            // Default states and otherwise
            $urlRouterProvider.otherwise('/');

            // State Configuration
            var stateCfg = statehelperConfigProvider;
            stateCfg.config.$stateProvider = $stateProvider;
            stateCfg.config.docTitle = 'Proyecto Hira: ';
        }

        configureRouting();
    }

    angular.module('hiraApp.core')
        .config(configure);

})());
