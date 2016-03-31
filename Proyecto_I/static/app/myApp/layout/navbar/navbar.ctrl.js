((function() {

    'use strict';

    /*@ngInject*/
    function Navbar(datacontext) {
        var vm = this;

        /*PRIVATE FUNCTIONS*/
        function getInfo(forceRemote) {
            var options = {
                forceRemote: forceRemote,
                manager: 'main',
                filter: {
                    find: [{
                        key: 'level',
                        value: 0
                    }]
                }
            };

            datacontext.views.list(options).then(function(views) {
                vm.views = views;
                vm.dataLoaded = true;
            });
        }

        function activate() {
            //getInfo(false);
            vm.views = [
                {
                    name: 'dashboard.cms',
                    title: 'CMS'
                },
                {
                    name: 'dashboard.crm',
                    title: 'CRM'
                },
                {
                    name: 'dashboard.bd',
                    title: 'BD'
                },
                {
                    name: 'dashboard.chat',
                    title: 'Chat'
                }
            ];
        }

        /*DEFINITION OF VARIABLES*/

        vm.dataLoaded = false;
        vm.views = [];
        vm.showMenu = false;

        activate();

    }

    angular.module('hiraApp.navbar')
        .controller('Navbar', Navbar);

})());
