
$("#messages").on("click", ".fa-star", async function(event){
  event.preventDefault();

  const $target = $(event.target);
  
  if ($tgt.hasClass("fas")) {
    $tgt.closest("i").toggleClass("fas far");
  } else {
    $tgt.closest("i").toggleClass("fas far");
  }

});
