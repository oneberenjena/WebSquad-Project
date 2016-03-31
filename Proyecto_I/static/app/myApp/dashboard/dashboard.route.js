((function () {

    'use strict';

    function getStates() {
        return [
            {
                name: 'dashboard',
                config: {
                    url: '/',
                    data: {
                        authenticate: true
                    },
                    views: {
                        '' : {
                            controller: 'DashboardCtrl',
                            controllerAs: 'vm',
                            templateUrl: 'app/myApp/dashboard/dashboard.html'
                        },
                        'manager@dashboard' : {
                            template: '<div ui-view="" layout="row" flex></div>'
                        },
                        'navbar@dashboard' : {
                            controller: 'Navbar',
                            controllerAs: 'vm',
                            templateUrl: 'app/myApp/layout/navbar/navbar.html'
                        }
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
        .module('hiraApp.dashboard')
        .run(stateConfig);

})());