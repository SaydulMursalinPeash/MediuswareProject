<template>
  <section>
    <div class="row">
      <div class="col-md-6">
        <div class="card shadow mb-4">
          <div class="card-body">
            <div class="form-group">
              <label for="">Product Name</label>
              <input type="text" v-model="product_name" placeholder="Product Name" class="form-control">
            </div>
            <div class="form-group">
              <label for="">Product SKU</label>
              <input type="text" v-model="product_sku" placeholder="Product Name" class="form-control">
            </div>
            <div class="form-group">
              <label for="">Description</label>
              <textarea v-model="description" id="" cols="30" rows="4" class="form-control"></textarea>
            </div>
          </div>
        </div>

        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Media</h6>
          </div>
          <div class="card-body border">
            <picture-input ref="pictureInput" size="2" @change="onChange"></picture-input>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Variants</h6>
          </div>
          <div class="card-body">
            <div class="row" v-for="(item,index) in product_variant">
              <div class="col-md-4">
                <div class="form-group">
                  <label for="">Option</label>
                  <select v-model="item.option" class="form-control">
                    <option v-for="variant in variants":value="variant.id">
                      {{ variant.title }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-8">
                <div class="form-group">
                  <label v-if="product_variant.length != 1" @click="product_variant.splice(index,1); checkVariant"
                         class="float-right text-primary"
                         style="cursor: pointer;">Remove</label>
                  <label v-else for="">.</label>
                  <input-tag v-model="item.tags" @input="checkVariant" class="form-control"></input-tag>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer" v-if="product_variant.length < variants.length && product_variant.length < 3">
            <button @click="newVariant" class="btn btn-primary">Add another option</button>
          </div>

          <div class="card-header text-uppercase">Preview</div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                <tr>
                  <td>Variant</td>
                  <td>Price</td>
                  <td>Stock</td>
                </tr>
                </thead>
                <tbody>
                <tr v-for="variant_price in product_variant_prices">
                  <td>{{ variant_price.title }}</td>
                  <td>
                    <input type="text" class="form-control" v-model="variant_price.price">
                  </td>
                  <td>
                    <input type="text" class="form-control" v-model="variant_price.stock">
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button @click="saveProduct" type="submit" class="btn btn-lg btn-primary">Save</button>
    <button type="button" class="btn btn-secondary btn-lg">Cancel</button>
  </section>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import InputTag from 'vue-input-tag'
import axios from 'axios';
import pictureInput from 'vue-picture-input'

export default {
  components: {
    pictureInput,
    InputTag
  },
  props: {
    variants: {
      type: Array,
      required: true
    }
  },
  data() {
    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken=getCookie("csrftoken");
    return {
      product_name: '',
      product_sku: '',
      description: '',
      images: [],
      product_variant: [
        {
          option: this.variants[0].id,
          tags: []
        }
      ],
      product_variant_prices: [],
      dropzoneOptions: {
        //url: 'https://httpbin.org/post',
        url:'http://127.0.0.1:8000/product/create/',
        thumbnailWidth: 150,
        maxFilesize: 2,
        headers: { "My-Awesome-Header": "header value" },
        //"X-CSRFToken":csrftoken,
      
      },
    }
  },
  //File uploaded function
  
  methods: {
    // it will push a new object into product variant
    newVariant() {
      let all_variants = this.variants.map(el => el.id)
      let selected_variants = this.product_variant.map(el => el.option);
      let available_variants = all_variants.filter(entry1 => !selected_variants.some(entry2 => entry1 == entry2))
      // console.log(available_variants)

      this.product_variant.push({
        option: available_variants[0],
        tags: []
      })
    },

    onChange(image){
      console.log("Image Selected");
      if(image){
        console.log("image Loaded..");
        this.images[0]=image;
      }
      else{
        console.log("Failed load Image..");
      }
    },


    afterComplete(file) {
      console.log(file);
      this.images=file.vue2Dropzone;
      console.log("Success");
    },

    // check the variant and render all the combination
    checkVariant() {
      let tags = [];
      this.product_variant_prices = [];
      this.product_variant.filter((item) => {
        tags.push(item.tags);
      })

      this.getCombn(tags).forEach(item => {
        this.product_variant_prices.push({
          title: item,
          price: 0,
          stock: 0
        })
      })
    },

    // combination algorithm
    getCombn(arr, pre) {
      pre = pre || '';
      if (!arr.length) {
        return pre;
      }
      let self = this;
      let ans = arr[0].reduce(function (ans, value) {
        return ans.concat(self.getCombn(arr.slice(1), pre + value + '/'));
      }, []);
      return ans;
    },

    
    // store product into database
    saveProduct() {

      let product = {
        title: this.product_name,
        sku: this.product_sku,
        description: this.description,
        product_variant: this.product_variant,
        product_variant_prices: this.product_variant_prices,
        product_image:this.images,
      }
      

      
      console.log(product)
      
      function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
      const csrftoken = getCookie('csrftoken');
      axios({
        method:"post",
        url:"http://127.0.0.1:8000/product/product",
        data:product,
        headers:{
          "X-CSRFToken":csrftoken
        }
      }).then((resp)=>{
        console.log(resp);
      }).catch((e)=>{
        console.log(e);
      })

    }


  },
  mounted() {
    console.log('Component mounted.')
  }
}
</script>
