((function() {
    'use strict';

    function getStates() {
        return [{
            name: 'dashboard.chat',
            config: {
                url: '^/chat',
                views: {
                    '@dashboard': {
                        templateUrl: 'app/myApp/managers/chat/chat.html',
                        controller: 'DashboardChatCtrl',
                        controllerAs: 'vm'
                    },
                    'sidebar@dashboard.chat': {
                        controller: 'DashboardChatSidebarCtrl',
                        templateUrl: 'app/myApp/managers/chat/sidebar/sidebar.html',
                        controllerAs: 'vm'
                    },
                    'contactbar@dashboard.chat': {
                        controller: 'DashboardChatContactbarCtrl',
                        templateUrl: 'app/myApp/managers/chat/contactbar/contactbar.html',
                        controllerAs: 'vm'
                    },
                    'board@dashboard.chat': {
                        controller: 'DashboardChatBoardCtrl',
                        controllerAs: 'vm',
                        templateUrl: 'app/myApp/managers/chat/board/board.html'
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
        .module('hiraApp.dashboard.chat')
        .run(stateConfig);

})());
