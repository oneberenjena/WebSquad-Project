((function () {
    'use strict';

    // Must configure via the statehelperConfigProvider

    /*@ngInject*/
    function statehelper(common, statehelperConfig, datacontext) {
        var service = {};

        var handlingRouteChangeError = false;

        var stateCounts = {
            errors: 0,
            changes: 0
        };

        var states = [];

        var $stateProvider = statehelperConfig.config.$stateProvider;

        var $rootScope = common.$rootScope;

        var $state = common.$state;


        ///////////////


        function handleRoutingErrors() {
            // Route cancellation:
            // On routing error, go to the dashboard.
            // Provide an exit clause if it tries to do it twice.
            $rootScope.$on('$stateChangeError', function () {
                if (handlingRouteChangeError) {
                    return;
                }
                stateCounts.errors += 1;
                handlingRouteChangeError = true;
                /*var destination = (current && (current.title || current.name || current.loadedTemplateUrl)) ||
                    'unknown target';
                var msg = 'Error routing to ' + destination + '. ' + (rejection.msg || '');
                logger.warning(msg, [current]);*/
                $state.go('home');
            });
        }

        function updateDocTitle() {
            $rootScope.$on('$stateChangeSuccess', function (event, current) {
                stateCounts.changes += 1;
                handlingRouteChangeError = false;
                var title = statehelperConfig.config.docTitle + ' ' + (current.title || '');
                $rootScope.title = title; // data bind to <title>
            });
        }

        function init() {
            handleRoutingErrors();
            updateDocTitle();
        }



        service.getStates = function () {
            var i, state;

            for (i = 0; i < $state.get().length; i += 1) {
                state = $state.get()[i];
                if (state.name.length > 0 && !state.abstract) {
                    states.push($state.get()[i]);
                }
            }

            return states;
        };

        service.setInfo = function (view) {
            return datacontext.blocks.getInfo(false, {view: view}).then(function (info) {
                if (info) {
                    return info;
                }

                return {};
            });
        };

        service.configureStates = function (states) {
            states.forEach(function (state) {
                state.config.controllerAs = 'vm';
                /*state.config.resolve =
                    angular.extend(state.config.resolve || {}, statehelperConfig.config.resolveAlways);*/
                $stateProvider.state(state.name, state.config);
            });
        };

        service.stateCounts = stateCounts;

        init();

        return service;
    }

    function statehelperConfig() {
        /* jshint validthis:true */
        this.config = {

            // These are the properties we need to set
            //$urlstaterProvider: undefined
            // docTitle: ''
            // resolveAlways: {ready: function(){ } }
        };

        this.$get = function () {
            return {
                config: this.config
            };
        };
    }

    angular
        .module('blocks.stateManager')
        .provider('statehelperConfig', statehelperConfig)
        .factory('statehelper', statehelper);

})());