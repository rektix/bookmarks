function addFolder(value){
    hideAll()
    $("#add-folder").removeClass("hidden");
    $("#folder_parent_folder").val(value.toString());
}

function addBookmark(value){
    hideAll()
    $("#add-bookmark").removeClass("hidden");
    $("#bookmark_parent_folder").val(value.toString());
}

function removeFolder(value){
    hideAll()
    $("#remove-folder").removeClass("hidden");
    $("#folder_id").val(value);
}

function removeBookmark(value){
    hideAll()
    $("#remove-bookmark").removeClass("hidden");
    $("#bookmark_id").val(value);
}

function editFolder(id,name,parent){
    hideAll()
    $("#update-folder").removeClass("hidden");
    $("#folder_id_update").val(id);
    $("#folder_name_update").val(name.toString());
    $("#folder_parent_folder_update").val(parent.toString());
}

function editBookmark(id,name,folder,link,description){
    hideAll()
    $("#update-bookmark").removeClass("hidden");
    $("#bookmark_id_update").val(id);
    $("#bookmark_name_update").val(name.toString());
    $("#bookmark_parent_folder_update").val(folder.toString());
    $("#link_update").val(link.toString());
    $("#description_update").val(description.toString());
}

function hideAll(){
    cover = $("#cover");
    if (cover.css("display") == 'block'){
        cover.css("display", "none");
    } else {
        cover.css("display", "block");
    }
    
    $(".form").addClass("hidden")
}

$(document).on("click",".show", function(){
    divs = $(this).siblings("div");
    if (divs.hasClass("hidden")) {
        divs.removeClass("hidden");
        $(this).children('i').removeClass("fa-chevron-up");
        $(this).children('i').addClass("fa-chevron-down");
        
    } else {
        divs.addClass("hidden");
        $(this).children('i').removeClass("fa-chevron-down");
        $(this).children('i').addClass("fa-chevron-up");
    }
})