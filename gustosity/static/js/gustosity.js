$(function () {

    // Models
    //************
    window.Ingredient = Backbone.Model.extend({
        defaults: function() {
            return {
                recipe: urlRecipe
            }
        }
    });

    window.Step = Backbone.Model.extend({
        defaults: function() {
            return {
                recipe: urlRecipe
            }
        }
    });

    // Collections
    //************
    window.IngredientCollection = Backbone.Collection.extend({
        model: Ingredient,
        url: "/api/ingredients",
        parse: function(response) {
            return response.results;
        }
    });

    window.StepCollection = Backbone.Collection.extend({
        model: Step,
        url: "/api/steps",
        parse: function(response) {
            return response.results;
        }
    });

    window.IngredientListItemView = Backbone.View.extend({

        tagName: "li",

        template: _.template($('#ingredient-template').html()),

        events: {
            "click .view"  : "edit",
            "click a.destroy": "confirm_delete",
            "keypress .edit": "updateOnEnter",
            "click .save-btn": "close",
            "click .cancel-btn": "cancel",
            "click button.delete": "clear"
        },

        initialize: function() {
              this.listenTo(this.model, 'change', this.render);
              this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function(eventName) {
            $(this.el).html(this.template(this.model.toJSON()));
            this.div = this.$('.edit');
            return this;
        },

        // Switch this view into `"editing"` mode, displaying the input field.
        edit: function() {
          this.$el.addClass("editing");
          this.$('.name').focus();
        },

        // Close the `"editing"` mode, saving changes to the todo.
        close: function() {
          var name = this.$('.name').val();
          var optional = false;
          if (this.$('.optional').attr('checked')) {
            optional = true;
          }
          if (!name) {
            this.$('.name').clear();
          } else {
            this.model.save({name: name, optional: optional});
            this.$el.removeClass("editing");
          }
        },

        cancel: function() {
            this.$('.name').val(this.model.get('name'));
            this.$('.optional').attr('checked', this.model.get('optional'));
            this.$el.removeClass("editing");
        },

        // If you hit `enter`, we're through editing the item.
        updateOnEnter: function(e) {
            if (e.keyCode == 13) this.close();
        },

        confirm_delete: function(e) {
            var _this = this;
            var template = _.template($("#delete-ingredient-template").html());
            $("#modal").html(template({'ingredient': this.model.get('name')}));
            $("#modal").modal();
            $("#modal .delete").click(function(e) {
                e.preventDefault();
                _this.clear();
                $("#modal").modal('hide');
            });
            e.stopPropagation();
        },

        // Remove the item, destroy the model.
        clear: function() {
            this.model.destroy({
                wait: true,
                success: function() {
                    // alert("Ingredient deleted successfully");
                }
            });
        }
    });

    window.StepListItemView = Backbone.View.extend({

        tagName: "li",

        template: _.template($('#step-template').html()),

        events: {
            "click .edit-btn": "edit",
            "click .save-btn": "close",
            "click .cancel-btn": "cancel",
            "click .destroy": "confirm_delete",
            "click button.delete": "clear"
        },

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function(eventName) {
            $(this.el).html(this.template(this.model.toJSON()));
            this.input = this.$('.desc');
            _.defer( setUploader, this.model );
            return this;
        },

        // Switch this view into `"editing"` mode, displaying the input field.
        edit: function() {
          this.$el.addClass("editing");
          this.input.focus();
        },

        // Close the `"editing"` mode, saving changes to the todo.
        close: function() {
          var value = this.input.val();
          if (!value) {
            this.clear();
          } else {
            this.model.save({description: value});
            this.$el.removeClass("editing");
          }
        },

        cancel: function() {
            this.input.val(this.model.get('description'));
            this.$el.removeClass("editing");
        },

        // If you hit `enter`, we're through editing the item.
        updateOnEnter: function(e) {
            if (e.keyCode == 13) this.close();
        },

        confirm_delete: function() {
            var _this = this;
            var template = _.template($("#delete-step-template").html());
            $("#modal").html(template({
                'description': this.model.get('description'),
                'imgsrc': this.model.get('thumb')
            }));
            $("#modal").modal();
            $("#modal .delete").click(function(e) {
                e.preventDefault();
                _this.clear();
                $("#modal").modal('hide');
            });

        },

        // Remove the item, destroy the model.
        clear: function() {
            this.model.destroy({
                wait: true,
                success: function() {
                    /* alert("Ingredient deleted successfully");*/
                }
            });
        }
    });

    // Create our global collections
    var Ingredients = new IngredientCollection();
    var Steps = new StepCollection();

    window.IngredientsEditView = Backbone.View.extend({

        el: $("#ingredientsapp"),

        // Delegated events for creating new items, and clearing completed ones.
        events: {
          "keypress #new-ingredient":  "createIngredientOnEnter",
          'click #addnewingredient': 'create'
        },

        initialize: function() {
            this.ingredient_input = this.$("#new-ingredient");
            this.optional_input = this.$("#new-optional");
            this.listenTo(Ingredients, 'add', this.addOneIngredient);
            this.listenTo(Ingredients, 'reset', this.addAllIngredients);
            this.listenTo(Ingredients, 'all', this.render);
            Ingredients.fetch({data: $.param({recipe: recipeId})});
        },

        addOneIngredient: function(ingredient) {
            var view = new IngredientListItemView({model: ingredient});
            this.$("#ingredients-list").append(view.render().el);
        },

        addAllIngredients: function() {
            Ingredients.each(this.addOneIngredient);
        },

        // If you hit return in the main input field, create new **Todo** model,
        // persisting it to *localStorage*.
        createIngredientOnEnter: function(e) {
          if (e.keyCode != 13) return;
          if (!this.ingredient_input.val()) return;
          this.create();
        },

        create: function() {
          Ingredients.create({
            full_name:'',
            name: this.ingredient_input.val(),
            optional: this.optional_input.attr('checked')
          });
          this.ingredient_input.val('');
          this.optional_input.attr('checked', false);
        }

    });

    window.StepsEditView = Backbone.View.extend({

        el: $("#stepsapp"),

        // Delegated events for creating new items, and clearing completed ones.
        events: {
          "keypress #new-step": "createStepOnEnter"
        },

        initialize: function() {
            this.step_input = this.$("#new-step");
            this.listenTo(Steps, 'add', this.addOneStep);
            this.listenTo(Steps, 'reset', this.addAllSteps);
            this.listenTo(Steps, 'all', this.render);
            Steps.fetch({data: $.param({recipe: recipeId})});
        },

        addOneStep: function(step) {
            var view = new StepListItemView({model: step});
            this.$("#steps-list").append(view.render().el);
            setUploader(step);
        },

        addAllSteps: function() {
            Steps.each(this.addOneStep);
        },

        createStepOnEnter: function(e) {
          if (e.keyCode != 13) return;
          if (!this.step_input.val()) return;
          Steps.create({
                description: this.step_input.val()
            }, {
                wait: true
            });
          this.step_input.val('');
        }

    });

    setUploader = function(step) {
        var thumb = step.get('thumb');
        if (thumb) {
            var step_image_id = '#step-image-' + step.id;
            $(step_image_id).attr('src', thumb);
        }
        new qq.FineUploader({
          element: $('#uploader-' + step.id)[0],
          button: $('#upload-btn-' + step.id)[0],
          request: {
            endpoint: '/upload/',
            params: {
                'recipe': recipeSlug,
                'user': recipeUser,
                'step': step.id
              }
          },
          multiple: false,
          validation: {
            allowedExtensions: ['jpeg', 'jpg', 'gif', 'png'],
            sizeLimit: 5120000 // 50 kB = 50 * 1024 bytes
          },
          callbacks: {
            onComplete: function(id, fileName, responseJSON) {
              if (responseJSON.success) {
                var step_image_id = '#step-image-' + responseJSON.id;
                $(step_image_id).attr('src', responseJSON.thumb);
              }
            }
          },
          debug: true
        });
    };
    // Source: http://stackoverflow.com/a/12336703
    // fixed with some code from http://10kblogger.wordpress.com/2012/05/28/a-restful-password-locker-with-django-and-backbone-js-part-4/
    /* alias away the sync method */

    Backbone._sync = Backbone.sync;
    /* define a new sync method */
    Backbone.sync = function(method, model, options) {
        /* only need a token for non-get requests */
        if (method == 'create' || method == 'update' || method == 'delete') {
            // CSRF token value is in an embedded meta tag
            var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
            options.beforeSend = function(xhr){
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            };
        }
        /* proxy the call to the old sync method */
        return Backbone._sync(method, model, options);
    };

});

/*================================================================*/
/*  MOBILE NAV TRIGGER
/*================================================================*/
$(document).ready(function(){
    $('.mobile_nav a').click(function(){
        console.log('asdf');
        $('#main_menu').slideToggle(400);
        $(this).toggleClass('active'); return false;
    });
});

/*================================================================*/
/*  BACK TO TOP
/*================================================================*/

$(document).ready(function(){

    // hide .backToTop first
    $(".backToTop").hide();

    // fade in .gototop
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.backToTop').fadeIn();
            } else {
                $('.backToTop').fadeOut();
            }
        });

        // scroll body to 0px on click
        $('.backToTop a').click(function () {
            $('body,html').animate({
                scrollTop: 0
            }, 800);
            return false;
        });
    });

});
