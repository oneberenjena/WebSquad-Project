((function() {
    'use strict';

    function getStates() {
        return [{
            name: 'dashboard.chat.board.profile',
            config: {
                views: {
                    '@dashboard.chat': {
                        templateUrl: 'app/myApp/managers/chat/board/profile/profile.html',
                        controller: 'DashboardChatProfileCtrl',
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
        .module('hiraApp.dashboard.chat.profile')
        .run(stateConfig);

})());
