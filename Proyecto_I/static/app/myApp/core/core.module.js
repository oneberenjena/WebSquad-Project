((function () {

    'use strict';

    angular.module('hiraApp.core', [
        // Angular dependencies
        'ngCookies', 'ngResource', 'ngSanitize', 'ngMaterial',
        // hiraApp blocks maid by us
        'blocks.stateManager',
        // 3rd party dependencies
        'ui.router', 'ngAnimate', 'textAngular',
        'LocalStorageModule', 'ngMdIcons'
    ]);

})());