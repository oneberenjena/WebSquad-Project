((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatCtrl(common, ChatService, $mdSidenav) {
        var vm = this;
        var $state = common.$state;

        /*PRIVATE FUNCTIONS*/
        function activate() {
            vm.show = ChatService.data.show;
        }

        /*DEFINITION OF VARIABLES*/
        activate();


    }

    angular.module('hiraApp.dashboard.chat')
        .controller('DashboardChatCtrl', DashboardChatCtrl);

})());