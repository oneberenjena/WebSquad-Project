((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatContactbarCtrl(common, datacontext, $mdSidenav, ChatService, Auth, $http) {
        var vm = this;
        var $state = common.$state;
        var currentUser = Auth.getCurrentUser();

        /*PRIVATE FUNCTIONS*/
        function activate() {
            getContacts(false);

            datacontext.groups.list({forceRemote:true,manager:"groups"}).then(function(res){
                console.log(res);
            });

            datacontext.chats.list({forceRemote:true,manager:"groups"}).then(function(res){
                console.log(res);
            });
            //datacontext.memberships.remove("groups",2);
            //datacontext.groups.remove("groups",1);

            /*

             datacontext.groups.getById(1).then(function(res){
             console.log(res);
             });

             */
            /*datacontext.memberships.list({forceRemote:false,manager:"groups"}).then(function(res){
                console.log(res.data1);
            });
            /!*$http.post('chat/AElimMiembro',{idGrupo:2,idUsuario:4});

            $http.post('chat/ASalirGrupo',{idGrupo:2});*!/

            datacontext.groups.list({forceRemote:false,manager:"groups"}).then(function(res){
                console.log(res);
            });*/

            /*

             datacontext.groups.list({forceRemote:false,manager:"groups"}).then(function(res){
             vm.groups = res.data1;
             console.log(res);
             });*/

            /*$http.post('chat/AElimContacto',{idAmigo:4});

            datacontext.contacts.list({forceRemote:false,manager:"groups"}).then(function(res){
                vm.groups = res.data1;
                console.log(res);
            });
            */
        }

        function getContacts(forceRemote){
            var options = {
                forceRemote: forceRemote,
                manager: "contacts"
            };

            datacontext.contacts.list(options).then(function(res){
                vm.contacts = res.data1;
            });
        }

        /*DEFINITION OF VARIABLES*/
        activate();

        function goBack(){
            ChatService.showChats();
        }

        function selectContact(chat){
            ChatService.selectChat(chat);
            common.$state.go('dashboard.chat.board.messages');

            datacontext.chats.create("chats",{id:1,type:"grupo"}).then()
        }

        function toggleMenu(){
            $mdSidenav("contacts").toggle();
        }

        vm.toggleMenu = toggleMenu;

        vm.goBack = goBack;
        vm.selectContact = selectContact;
    }

    angular.module('hiraApp.dashboard.chat.contactbar')
        .controller('DashboardChatContactbarCtrl', DashboardChatContactbarCtrl);

})());