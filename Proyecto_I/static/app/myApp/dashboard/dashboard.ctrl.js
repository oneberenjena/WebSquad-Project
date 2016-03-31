(function() {

    'use strict';

    /*@ngInject*/
    function DashboardCtrl(common) {
        var vm = this,
            $rootScope = common.$rootScope,
            $stateParams = common.$stateParams,
            states = {};

        vm.items = [{
            'name': 'Base de Datos',
            'icon': 'fa-database'
        }, {
            'name': 'Vistas',
            'icon': 'fa-file-code-o'
        }, {
            'name': 'Redes Sociales',
            'icon': 'fa-bar-chart'
        }];


        /*PRIVATE FUNCTIONS*/
        function activate() {}

        vm.actualHe = common.$window.innerHeight;

        /*DEFINITION OF VARIABLES*/

        activate();
    }

    angular.module('hiraApp.dashboard')
        .controller('DashboardCtrl', DashboardCtrl);

}());
