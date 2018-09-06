<template>
      <main role="main">
          

    <section class="jumbotron text-center">
      <div class="container">
        <h1 class="jumbotron-heading">AI写真検索</h1>
        <p class="align-items-center">
          <form class="form-inline row justify-content-around" method="get">
            <input class="form-control form-control-lg mb-2 col-7" type="text" placeholder="Input Amazonian's name or Tag" aria-label="Search" name="search" v-bind:value="search_text">
            <div class="col-1"></div>
            <button class="btn btn-outline-dark btn-lg mb-2 col-3" type="submit">Search</button>
          </form>
        </p>
        <h3>{{ pagination.total_items }} Photos</h3>
      </div>
    </section>


    <div class="album py-5 bg-dark">

      <template v-if="pagination.previous">
      <div class="container">
        <a v-bind:href="pagination.previous" class="btn btn-outline-warning btn-lg btn-block mb-4" role="button">
          <strong>Previous</strong>
        </a>
      </div>
      </template>

      <div class="container">
        <div class="row">

              <div v-for="item in items" class="col-md-4 col-xl-3">
                <div class="card mb-4 shadow-sm">
                  <div class="photo">
                    <a v-bind:href="item.image_uri" v-bind:data-lightbox="item.name" v-bind:data-title="item.name">
                        <img class="card-img-top" v-bind:src="item.thumbnail_uri" v-bind:alt="item.name">
                    </a>
                  </div>
                  <div class="card-body">
                    <p class="card-text">
                      <a v-for="tag in item.name_tags" v-bind:href="tag.text" class="badge badge-pill badge-warning">{{ tag.text }} <span class="debug">{{ tag.confidence }}, {{ tag.similarity }}</span></a>
                      <a v-for="tag in item.emotion_tags" v-bind:href="tag.text" class="badge badge-pill badge-success">{{ tag.text }} <span class="debug">{{ tag.count }}</span></a>
                      <a v-for="tag in item.tags" v-bind:href="tag.text" class="badge badge-pill badge-secondary">{{ tag.text }} <span class="debug">{{ tag.confidence }}</span></a>
                    </p>
                  </div>
                </div>
              </div>

        </div>
      </div>

      <template v-if="pagination.previous">
      <div class="container">
        <a v-bind:href="pagination.next" class="btn btn-outline-warning btn-lg btn-block" role="button">
          <strong>Next</strong>
        </a>
      </div>
      </template>

    </div>

   </main>
</template>

<script>
export default {
  name: 'PhotoManager',
  data: function() {
    return {
      msg: 'Welcome to Your Vue.js App',
      items: [{name: 'test', image_uri: 'hoge', thumbnail_uri: 'fuga'}],
      search_text: '',
      pagination: {total_items: 3}
    };
  }
};
</script>

<style scoped>
</style>
