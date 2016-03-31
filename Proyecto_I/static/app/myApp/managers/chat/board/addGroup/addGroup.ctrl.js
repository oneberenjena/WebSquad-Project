((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatAddGroupCtrl(common, datacontext, Auth) {
        var vm = this;
        var currentUser = Auth.getCurrentUser();
        vm.group = {};

        function activate() {
            getContacts(false);
        }

        function getContacts(forceRemote){
            var options = {
                forceRemote: forceRemote,
                manager: "contacts",
                filter: {
                    find: [{
                        key: 'userId',
                        value: currentUser._id
                    }]
                }
            };

            datacontext.contacts.list(options).then(function(res){
                vm.contacts = res.data1;
            });

        }
        
        /*DEFINITION OF VARIABLES*/
        activate();

        function addGroup(){
            var size = vm.contacts.length,
                members = [];

            for (var i = 0; i < size; i++) {
                if (vm.contacts[i].wanted) {
                    members.push(vm.contacts[i].idContacto);
                }
            }


            datacontext.groups.create("groups",vm.group).then(function(res){
                var size = members.length;

                for (var i = 0; i < size; i++) {
                    // define the current function
                    var usuario = members[i];
                    (function(usuario){
                        datacontext.memberships.create("memberships",{idGrupo:res,idUsuario:usuario});
                    })(usuario);
                }

                /*var size = res.members.length;
                var chat = {};
                var chats = [];

                for (var i = 0; i < size; i++){
                    chat = {};
                    chat.info = res;
                    chat.type = "group";
                    chat.messages = [];
                    chat.userId = res.members[i];
                    chats.push(chat);
                }

                datacontext.chats.create("chats",chats);*/
            });
        }

        vm.addGroup = addGroup;
    }

    angular.module('hiraApp.dashboard.chat.addGroup')
        .controller('DashboardChatAddGroupCtrl', DashboardChatAddGroupCtrl);

})());