// This script initializes the TinyMCE rich text editor.
// Make sure to get your own API key from tiny.cloud for production use.
tinymce.init({
  selector: "textarea#content-editor",
  plugins:
    "preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons",
  menubar: "file edit view insert format tools table help",
  toolbar:
    "undo redo | bold italic underline strikethrough | fontfamily fontsize blocks | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl",
  skin: window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "oxide-dark"
    : "oxide",
  content_css: window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "default",
  height: 600,
  image_caption: true,
  quickbars_selection_toolbar:
    "bold italic | quicklink h2 h3 blockquote quickimage quicktable",
  noneditable_class: "mceNonEditable",
  toolbar_mode: "sliding",
  contextmenu: "link image table",
  content_style: `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      body { font-family: 'Inter', sans-serif; background-color: #161626; color: #f0f0f5; }
      a { color: #00e5ff; }
      blockquote { border-left: 4px solid #8e44ad; padding-left: 20px; margin-left: 0; font-style: italic; }
      pre { background: #0d0d1a; padding: 20px; border-radius: 8px; font-family: 'JetBrains Mono', monospace; }
    `,
});
