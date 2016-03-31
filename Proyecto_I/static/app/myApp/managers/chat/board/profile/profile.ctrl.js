((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatProfileCtrl(common, ChatService) {
        var vm = this;

        function activate() {
            vm.selected = ChatService.data.selected;
        }
        
        /*DEFINITION OF VARIABLES*/
        activate();
    }

    angular.module('hiraApp.dashboard.chat.profile')
        .controller('DashboardChatProfileCtrl', DashboardChatProfileCtrl);

})());