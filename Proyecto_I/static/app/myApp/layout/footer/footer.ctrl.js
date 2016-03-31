((function() {

    'use strict';

    /*@ngInject*/
    function Footer(datacontext) {
        var vm = this;

        /*PRIVATE FUNCTIONS*/
        function getInfo(forceRemote) {
            var options = {
                forceRemote: forceRemote,
                manager: 'footer',
                filter: {
                    find: [{
                        key: 'view',
                        value: 'footer'
                    }]
                }
            };

            datacontext.blocks.list(options).then(function(info) {
                vm.info = info;
                vm.dataLoaded = true;
            });
        }

        function activate() {
            getInfo(false);
        }

        /*DEFINITION OF VARIABLES*/
        vm.info = {};
        vm.dataLoaded = false;

        activate();
    }

    angular
        .module('hiraApp.footer')
        .controller('Footer', Footer);

})());
