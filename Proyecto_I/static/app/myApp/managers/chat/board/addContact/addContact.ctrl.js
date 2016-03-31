((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatAddContactCtrl(common,datacontext,Auth) {
        var vm = this;
        var currentUser = Auth.getCurrentUser();
        vm.contact = {};

        function activate() {

        }
        
        /*DEFINITION OF VARIABLES*/
        activate();

        function addContact(){
            var options = {
                forceRemote: true,
                filter: {
                    find: [{
                        key: 'correo',
                        value: vm.contact.correo
                    }]
                }
            };

            datacontext.users.list(options).then(function(res){
                if (!res[0]) {
                    alert("No hay nadie!");
                    return false;
                }
                else {
                    vm.contact.idUsuario = res[0].idUsuario;
                    datacontext.contacts.create("contacts",vm.contact);
                }
            });

            //

        }

        vm.addContact = addContact;
    }

    angular.module('hiraApp.dashboard.chat.addContact')
        .controller('DashboardChatAddContactCtrl', DashboardChatAddContactCtrl);

})());