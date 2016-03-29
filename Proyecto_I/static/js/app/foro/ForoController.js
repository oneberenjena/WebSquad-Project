socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/VComentariosPagina/:idPaginaSitio', {
                controller: 'VComentariosPaginaController',
                templateUrl: 'app/foro/VComentariosPagina.html'
            }).when('/VForo/:idForo', {
                controller: 'VForoController',
                templateUrl: 'app/foro/VForo.html'
            }).when('/VForos/:idUsuario', {
                controller: 'VForosController',
                templateUrl: 'app/foro/VForos.html'
            }).when('/VPublicacion/:idMensaje', {
                controller: 'VPublicacionController',
                templateUrl: 'app/foro/VPublicacion.html'
            });
}]);

socialModule.controller('VComentariosPaginaController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, foroService, identService) {
      $scope.msg = '';
      $scope.fPublicacion = {};

      foroService.VComentariosPagina({"idPaginaSitio":$routeParams.idPaginaSitio}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        if ($scope.fPublicacion.fecha) {
          $scope.fPublicacion.fecha=new Date($scope.fPublicacion.fecha);
        }

      });
      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };

      $scope.fPublicacionSubmitted = false;
      $scope.AComentar0 = function(isValid) {
        $scope.fPublicacionSubmitted = true;
        if (isValid) {
          
          foroService.AComentar($scope.fPublicacion).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VComentariosPagina.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
socialModule.controller('VForoController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'ngTableParams', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, ngTableParams, foroService, identService) {
      $scope.msg = '';
      foroService.VForo({"idForo":$routeParams.idForo}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


              var VPublicacion0Data = $scope.res.data0;
              if(typeof VPublicacion0Data === 'undefined') VPublicacion0Data=[];
              $scope.tableParams0 = new ngTableParams({
                  page: 1,            // show first page
                  count: 10           // count per page
              }, {
                  total: VPublicacion0Data.length, // length of data
                  getData: function($defer, params) {
                      $defer.resolve(VPublicacion0Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                  }
              });            


      });
      $scope.VPublicacion1 = function(idMensaje) {
        $location.path('/VPublicacion/'+idMensaje);
      };
      $scope.VForos2 = function(idUsuario) {
        $location.path('/VForos/'+idUsuario);
      };
      $scope.AElimForo3 = function(idForo) {
          
        foroService.AElimForo({"idForo":((typeof idForo === 'object')?JSON.stringify(idForo):idForo)}).then(function (object) {
          var msg = object.data["msg"];
          if (msg) flash(msg);
          var label = object.data["label"];
          $location.path(label);
          $route.reload();
        });};

      $scope.VPublicacion0 = function(idMensaje) {
        $location.path('/VPublicacion/'+((typeof idMensaje === 'object')?JSON.stringify(idMensaje):idMensaje));
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VForo.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
socialModule.controller('VForosController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'ngTableParams', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, ngTableParams, foroService, identService) {
      $scope.msg = '';
      $scope.fForo = {};

      foroService.VForos({"idUsuario":$routeParams.idUsuario}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


              var VForo0Data = $scope.res.data0;
              if(typeof VForo0Data === 'undefined') VForo0Data=[];
              $scope.tableParams0 = new ngTableParams({
                  page: 1,            // show first page
                  count: 10           // count per page
              }, {
                  total: VForo0Data.length, // length of data
                  getData: function($defer, params) {
                      $defer.resolve(VForo0Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                  }
              });            


      });
      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };

      $scope.fForoSubmitted = false;
      $scope.AgregForo2 = function(isValid) {
        $scope.fForoSubmitted = true;
        if (isValid) {
          
          foroService.AgregForo($scope.fForo).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

      $scope.VForo0 = function(idForo) {
        $location.path('/VForo/'+((typeof idForo === 'object')?JSON.stringify(idForo):idForo));
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VForos.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
socialModule.controller('VPublicacionController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, foroService, identService) {
      $scope.msg = '';
      $scope.fPublicacion = {};

      foroService.VPublicacion({"idMensaje":$routeParams.idMensaje}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        if ($scope.fPublicacion.fecha) {
          $scope.fPublicacion.fecha=new Date($scope.fPublicacion.fecha);
        }

      });
      $scope.VForo1 = function(idForo) {
        $location.path('/VForo/'+idForo);
      };

      $scope.fPublicacionSubmitted = false;
      $scope.APublicar0 = function(isValid) {
        $scope.fPublicacionSubmitted = true;
        if (isValid) {
          
          foroService.APublicar($scope.fPublicacion).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VPublicacion.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
