((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatSidebarCtrl(common, datacontext, $mdSidenav, ChatService, Auth, $mdDialog) {
        var vm = this;
        var $state = common.$state;
        var currentUser = Auth.getCurrentUser();
        var originatorEv;

        vm.showContacts = false;

        /*PRIVATE FUNCTIONS*/
        function activate() {
            //getChats(false);
        }

        function getChats(forceRemote){
            console.log(currentUser);
            var options = {
                forceRemote: forceRemote,
                manager: "chats",
                filter: {
                    find: [{
                        key: 'idUsuario',
                        value: currentUser.idUsuario
                    }]
                }
            };

            datacontext.chats.list(options).then(function(res){
                vm.chats = res;
            });
        }

        /*DEFINITION OF VARIABLES*/
        activate();

        function newChat(){
            ChatService.showContacts();
        }

        function selectChat(chat){
            ChatService.selectChat(chat);
            common.$state.go('dashboard.chat.board.messages');
        }

        function toggleMenu(){
            $mdSidenav("contacts").toggle();
        }

        function openMenu($mdOpenMenu, ev) {
            originatorEv = ev;
            $mdOpenMenu(ev);
        };

        vm.openMenu = openMenu;
        vm.toggleMenu = toggleMenu;

        vm.newChat = newChat;
        vm.selectChat = selectChat;
    }

    angular.module('hiraApp.dashboard.chat.sidebar')
        .controller('DashboardChatSidebarCtrl', DashboardChatSidebarCtrl);

})());