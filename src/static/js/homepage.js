(function() {
        
  // state
  var isMultiFieldQueryActive = false

  // dropdown-toggle
  const toggleRef = document.getElementById("multi-field-query-action")
  const dropdownRef = document.getElementById("multi-field-query-dropdown")

  // search-box
  const mainQueryRef = document.getElementById("main_query")

  // input-fields
  const inputTitleRef = document.getElementById("pub_title")
  const inputAuthorRef = document.getElementById("pub_author")
  const inputCategoryRef = document.getElementById("pub_category")

  toggleRef.onclick = function() {
    isMultiFieldQueryActive = !isMultiFieldQueryActive
    
    if (isMultiFieldQueryActive) {
      dropdownRef.classList.add("active")

      mainQueryRef.removeAttribute("name") 
      mainQueryRef.setAttribute("disabled", "disabled")
      
      inputTitleRef.setAttribute("name", "title")
      inputAuthorRef.setAttribute("name", "author")
      inputCategoryRef.setAttribute("name", "category")
    } else {
      dropdownRef.classList.remove("active")

      mainQueryRef.setAttribute("name", "search")
      mainQueryRef.removeAttribute("disabled") 

      inputTitleRef.removeAttribute("name")
      inputAuthorRef.removeAttribute("name")
      inputCategoryRef.removeAttribute("name")
    }
  }

})();
