((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatMessagesCtrl(common, ChatService, $mdSidenav) {
        var vm = this;
        vm.message = {};

        function activate() {
            vm.messages = [
                {
                    content: "Prueba1",
                    author: "yo"
                },
                {
                    content: "Prueba1",
                    author: "luis"
                },
                {
                    content: "Prueba1",
                    author: "luis"
                },
                {
                    content: "Prueba1",
                    author: "luis"
                },
                {
                    content: "Prueba1",
                    author: "yo"
                },
                {
                    content: "Prueba1",
                    author: "yo"
                },
                {
                    content: "Prueba1",
                    author: "luis"
                },
                {
                    content: "Prueba1",
                    author: "yo"
                },
                {
                    content: "Prueba1",
                    author: "luis"
                },{
                    content: "Prueba1",
                    author: "luis"
                },
                {
                    content: "Prueba1",
                    author: "yo"
                },
                {
                    content: "Prueba1",
                    author: "yo"
                }
            ]

            vm.selected = ChatService.data.selected;
        }
        
        /*DEFINITION OF VARIABLES*/
        activate();
    }

    angular.module('hiraApp.dashboard.chat.messages')
        .controller('DashboardChatMessagesCtrl', DashboardChatMessagesCtrl);

})());