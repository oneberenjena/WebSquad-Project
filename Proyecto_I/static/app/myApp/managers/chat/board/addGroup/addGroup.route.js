((function() {
    'use strict';

    function getStates() {
        return [{
            name: 'dashboard.chat.board.addGroup',
            config: {
                views: {
                    '@dashboard.chat': {
                        templateUrl: 'app/myApp/managers/chat/board/addGroup/addGroup.html',
                        controller: 'DashboardChatAddGroupCtrl',
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
        .module('hiraApp.dashboard.chat.addGroup')
        .run(stateConfig);

})());
