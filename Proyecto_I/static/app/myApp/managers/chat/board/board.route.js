((function() {
    'use strict';

    function getStates() {
        return [{
            name: 'dashboard.chat.board',
            config: {
                params: {
                    chat: {}
                },
                abstract: true
            }
        }];
    }

    /* @ngInject */
    function stateConfig(statehelper) {
        statehelper.configureStates(getStates());
    }

    angular
        .module('hiraApp.dashboard.chat.board')
        .run(stateConfig);

})());
