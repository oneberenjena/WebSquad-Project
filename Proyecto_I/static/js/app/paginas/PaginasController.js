socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/VMiPagina/:idUsuario', {
                controller: 'VMiPaginaController',
                templateUrl: 'app/paginas/VMiPagina.html'
            }).when('/VPagina/:idUsuario', {
                controller: 'VPaginaController',
                templateUrl: 'app/paginas/VPagina.html'
            });
			$routeProvider.when('/VPaginaDetalle/:idUsuario', {
        	controller: 'VPaginaDetalleController',
        	templateUrl: 'app/paginas/VPaginaDetalle.html'
    		});
}]);

socialModule.controller('VMiPaginaController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'identService', 'paginasService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, identService, paginasService) {
      $scope.msg = '';
      $scope.idUsuario = $routeParams.idUsuario;
      paginasService.VMiPagina({"idUsuario":$routeParams.idUsuario}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }
        if ($scope.label) {
          $location.path($scope.label);
        }

      });
      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };

//Esto se lo copiamos
      $scope.VPagina2 = function(idUsuario) {
        $location.path('/VPagina/'+idUsuario);
      };

      $scope.VPagina1 = function(idUsuario) {
        $location.path('/VPagina/'+idUsuario);
      };

      $scope.VContactos2 = function(idUsuario) {
        $location.path('/VContactos/'+idUsuario);
      };
      $scope.VLogin0 = function() {
        $location.path('/VLogin');
      };

      $scope.fPaginaSubmitted = false;
      $scope.AModificarPagina0 = function(isValid) {
        $scope.fPaginaSubmitted = true;
        if (isValid) {
          
          paginasService.AModificarPagina($scope.fPagina).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VMiPagina.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);

socialModule.controller('VPaginaDetalleController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'identService', 'paginasService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, identService, paginasService) {
      $scope.pag = {};

      paginasService.VPagina({"idUsuario":$routeParams.idUsuario}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope.pag[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });

      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };

      $scope.fPaginaSubmitted = false;
      $scope.AModificarPagina0 = function(isValid) {
        $scope.fPaginaSubmitted = true;
        if (isValid) {
          
          paginasService.AModificarPagina($scope.fPagina).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VPagina.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);

socialModule.controller('VPaginaController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'identService', 'paginasService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, identService, paginasService) {
      $scope.msg = '';
      $scope.fPagina = {};

      paginasService.VPagina({"idUsuario":$routeParams.idUsuario}).then(function (object) {
        $scope.res = object.data;
        $scope.fPagina = {};
        for (var key in object.data) {
            $scope.fPagina[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }
        if ($scope.res.label) {
          $location.path($scope.res.label);
        }

      });
      $scope.VMiPagina = function(idUsuario) {
        $location.path('/VMiPagina/'+idUsuario);
      };
      $scope.VLogin0 = function() {
        $location.path('/VLogin');
      };

      $scope.VPagina1 = function(idUsuario) {
        $location.path('/VPagina/'+idUsuario);
      };

      $scope.VContactos2 = function(idUsuario) {
        $location.path('/VContactos/'+idUsuario);
      };
      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };

      $scope.fPaginaSubmitted = false;
      $scope.AModificarPagina0 = function(isValid) {
        $scope.fPaginaSubmitted = true;
        if (isValid) {
          
          paginasService.AModificarPagina($scope.fPagina).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VPagina.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
