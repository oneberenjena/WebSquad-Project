((function() {
    'use strict';

    function getStates() {
        return [{
            name: 'dashboard.chat.board.addContact',
            config: {
                views: {
                    '@dashboard.chat': {
                        templateUrl: 'app/myApp/managers/chat/board/addContact/addContact.html',
                        controller: 'DashboardChatAddContactCtrl',
                        controllerAs: 'vm'
                    }
                }
            }
        }];
    }

    /* @ngInject */
    function stateConfig(statehelper) {
        statehelper.configureStates(getStates());
    }

    angular
        .module('hiraApp.dashboard.chat.addContact')
        .run(stateConfig);

})());
