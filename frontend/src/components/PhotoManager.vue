<template>
<div class="photomanager">
  <section class="jumbotron text-center">
    <div class="container">
      <h1 class="jumbotron-heading">AI Photo Search</h1>
      <p class="align-items-center">
        <form class="form-inline row justify-content-around" method="get">
          <input class="form-control form-control-lg mb-2 col-12" type="text" placeholder="Input Name or Tag" aria-label="Search" name="search" v-model="search_text">
          <!--<button class="btn btn-outline-dark btn-lg mb-2 col-4" type="submit">Search</button>-->
        </form>
      </p>
      <h3> {{ countComputed }} Photos</h3>
    </div>
  </section>
  
  
  <div class="album py-5 bg-dark">
  
    <template v-if="pagination.previous >= 0">
      <div class="container">
        <a v-on:click="pagination.page -= 1" href="#" class="btn btn-outline-warning btn-lg btn-block mb-4" role="button">
          <strong>Previous</strong>
        </a>
      </div>
    </template>
  
    <div class="container">
      <div class="row">
        <div v-for="item in itemsComputed" class="col-md-4 col-xl-3">
          <div class="card mb-4 shadow-sm">
            <div class="photo">
              <a v-bind:href="item.image_uri" v-bind:data-lightbox="item.name" v-bind:data-title="item.name">
                <img class="card-img-top" v-bind:src="item.thumbnail_uri" v-bind:alt="item.name">
              </a>
            </div>
            <div class="card-body">
              <p class="card-text">
                <span v-for="tag in item.name_tags">
                  <a href="#" v-on:click="search_text=tag.text" class="badge badge-pill badge-warning">{{ tag.text }} <span class="debug">{{ tag.confidence }}, {{ tag.similarity }}</span>
                  </a>&nbsp; 
                </span>

                <span v-for="tag in item.emotion_tags">
                  <a href="#" v-on:click="search_text=tag.text" class="badge badge-pill badge-success">
                    {{ tag.text }}
                    <span class="debug">{{ tag.count }}</span>
                  </a>&nbsp;
                </span>
                
                <span v-for="tag in item.tags">
                  <a href="#" v-on:click="search_text=tag.text" class="badge badge-pill badge-secondary">
                    {{ tag.text }}
                    <span class="debug">{{ tag.confidence }}</span>
                  </a>&nbsp;
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <template v-if="pagination.next > 0">
      <div class="container">
        <a v-on:click="pagination.page += 1" href="#" class="btn btn-outline-warning btn-lg btn-block" role="button">
          <strong>Next</strong>
        </a>
      </div>
    </template>

  </div>
</div>

</template>

<script>
import axios from "axios"
const API_BASE_URL = 'https://53isy6xdtb.execute-api.us-west-2.amazonaws.com/Prod/'

export default {
  name: 'PhotoManager',
  data: function() {
    return {
      items: [],
      search_text: '',
      pagination: { total_items: 0, page:0, previous:-1, next:-1, page_size:24, count:0 },
    };
  },
  created: function() {
    this.search('', this.pagination.page, this.pagination.page_size)
  },
  methods: {
    search: function(tag, page, page_size) {
      var self = this;
      
      axios
      .get(API_BASE_URL + '/photos?tag=' + tag + '&page=' + page + '&page_size=' + page_size)
      .then(function(response) {
          self.items = response.data.data;
          self.pagination.next = response.data.pagination.next;
          self.pagination.previous = response.data.pagination.previous;
          console.dir(self.items);
          console.dir(self.pagination);
          console.log(self.items.length);
          
          return self.items.length;
      })
      .catch(function(error) {
          console.log(error);
      });
    }
  },
  computed: {
    countComputed: function(){
      this.pagination.count = this.search(this.search_text, this.pagination.page, this.pagination.page_size);
      return this.pagination.count
    },
    itemsComputed: function(){
      return this.items;
    }
  }
};
</script>

<style scoped>
</style>
