vim.api.nvim_create_autocmd("FileType", {
  pattern = "go",
  callback = function()
    vim.opt_local.shiftwidth = 8
    vim.opt_local.tabstop = 8
  end
})
