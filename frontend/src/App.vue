<template>
<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <link rel="icon" href="images/favicon.ico">

  <title>PhotoManager</title>

  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <!-- lightbox CSS -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/css/lightbox.css" rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="static/main.css" rel="stylesheet">
</head>

<body>

  <header>
    <div class="collapse bg-dark" id="navbarHeader">
      <div class="container">
        <div class="row">
          <div class="col-sm-8 col-md-7 py-4">
            <h4 class="text-white">About</h4>
            <p class="text-white">このページでは、AWSの人工知能・機械学習サービスの一つである <a class="text-warning" href="https://aws.amazon.com/jp/rekognition/" target="_blank">Amazon Rekognition</a> を利用し、事前に送っていただいたお子様の顔写真を元に、写真にだれが写っているか<strong>自動で</strong>判別しています（ただし、ラベルにはAmazonianの名前を入れてあります）。顔が隠れていたり、元の顔写真にあまりお顔が写っていなかったりなど、うまくいかないこともありますが、AIの力でお子様の写真を探す手助けになれば幸いです。<a class="text-warning" href="images/familyday2018_architecture20180828.png" data-lightbox="architecture">（参考アーキテクチャ図）</a></p>
            <div class="form-check form-check-inline">
              DebugMode: <input class="form-check-input" type="checkbox" id="debug_checkbox">
            </div>

          </div>
          <div class="col-sm-4 offset-md-1 py-4">
            <h4 class="text-white">Contact</h4>
            <h5 class="text-white">Web Site</h5>
            <ul class="list-unstyled text-muted">
              <li class="text-white">Please send us your feedback!</li>
              <li>midaisuk@ hariby@ toshiake@ juichika@</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="navbar navbar-dark bg-dark shadow-sm">
      <div class="container d-flex justify-content-between">
        <a href="/" class="navbar-brand d-flex align-items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
            <strong>PhotoManager</strong>
          </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarHeader" aria-controls="navbarHeader" aria-expanded="true" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
      </div>
    </div>
  </header>

  <div id="app">
    <router-view/>
  </div>

  <footer class="text-muted">
    <div class="container">
      <p class="float-right">
        <a href="#">Back to top</a>
      </p>
      <p>PhotoManager</p>
    </div>
  </footer>

  <!-- Bootstrap core JavaScript
    ================================================== -->
  <!-- Placed at the end of the document so the pages load faster -->
  <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/holder/2.9.4/holder.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/js/lightbox.min.js" type="text/javascript"></script>
  <script>
    var debug_checkbox = $('#debug_checkbox');
    debug_checkbox.on('click', function() {
      if($(this).is(':checked')) {
        $('.debug').css('display', 'inline');
      } else {
        $('.debug').css('display', 'none');
      }
    });
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=UA-124836673-1"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
  
    gtag('config', 'UA-124836673-1');
  </script>

</body>

</html>

</template>

<script>
export default {
  name: 'App'
}
</script>

<style>

</style>
