var numRecipes = 0;
var curPage = 0;
var numPages = 0;
var recipesPerPage = 6;
var recipes;

function searchRecipes(query) {
$.ajax({
  url: "https://recipe-scraper.herokuapp.com/api/title/" + query,
  success: getResults
});
}

function searchCuisine(query) {
$.ajax({
  url: "https://recipe-scraper.herokuapp.com/api/cuisine/" + query,
  success: getResults
});
}

function searchMin(query) {
  $.ajax({
    url: "https://recipe-scraper.herokuapp.com/api/prepTime/lt/" + query,
    success: getResults
  });
}

function searchMinMax(min, max) {
  $.ajax({
    url: "https://recipe-scraper.herokuapp.com/api/prepTime/gt/" + min + "/lt/" + max,
    success: getResults
  });
}

function getResults(data) {
  numRecipes = data.count;
  recipes = data.recipes;
  numPages = Math.ceil(recipes.length / recipesPerPage);
  curPage = 1;
  showResults(1);
  showNavBar(curPage, numPages);
}

function showResults(page) {
  var source = $("#recipe-template").html();
  var template = Handlebars.compile(source);
  var templateData = {recipe: []};

  var i = (page - 1) * recipesPerPage
  var orig_i = i;
  var count = 0;

  while (i < orig_i + recipesPerPage && i < numRecipes) {
    count++;
    templateData.recipe.push({
      templateURL: recipes[i].URL,
      templateTitle: recipes[i].title,
      templateImgURL: recipes[i].imgURL,
      templateCuisine: recipes[i].cuisine,
      templatePrepTime: recipes[i].prepTime,
      newRow: newRowNeeded(count),
      newRowEnd: newRowEndNeeded(count)});
    i++;
  }
  $("#results").html(template(templateData));
}

function showNavBar(cur, total) {
  var source = $("#nav-template").html();
  var template = Handlebars.compile(source);
  var templateData = {navpane: [
    {curPageNum: cur, totalPages: total}
  ]};
  $("#nav").html(template(templateData));

  $("#page-input").keyup(function(event){
    if (event.keyCode == 13) {
      var newPage = parseFloat($("#page-input").val());
      // Checking that user input is an integer within page bounds
        if (newPage >= 1 &&
          newPage <= numPages &&
          newPage == parseInt(newPage)) {
          curPage = newPage;
          showResults(curPage);
          showNavBar(curPage, numPages);
      }
    }
  });
}

function newRowNeeded(index) {
  if ( (index - 1) % 3 == 0) {
    return "<div class=\"row\">";
  } else {
    return;
  }
}

function newRowEndNeeded(index) {
  if ( (index % 3) == 0) {
    return "</div>";
  } else {
    return;
  }
}

$(document).ready(function(){
  $("#search-recipes-button").click(function(){
    searchRecipes($("#search-recipes").val());
  });

  $("#search-recipes").keyup(function(event){
    if(event.keyCode == 13){
        $("#search-recipes-button").click();
    }
  });

  $("#search-cuisine-button").click(function(){
    searchCuisine($("#search-cuisine").val());
  });

  $("#search-cuisine").keyup(function(event){
    if(event.keyCode == 13){
        $("#search-cuisine-button").click();
    }
  });

  $("#search-min-button").click(function(){
    searchMin($("#search-min").val());
  });

  $("#search-min").keyup(function(event){
    if(event.keyCode == 13){
        $("#search-min-button").click();
    }
  });

  $("#search-gt-lt-button").click(function(){
    searchMinMax($("#search-gt").val(), $("#search-lt").val());
  });

  $("#search-gt").keyup(function(event){
    if(event.keyCode == 13){
        $("#search-gt-lt-button").click();
    }
  });

  $("#search-lt").keyup(function(event){
    if(event.keyCode == 13){
        $("#search-gt-lt-button").click();
    }
  });
});
