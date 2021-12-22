#pragma once
#include <string>

typedef void *(*ImFileDialog_CreateTexture)(unsigned char *data, int w, int h, char fmt);
typedef void (*ImFileDialog_DeleteTexture)(void *texture);
namespace ifd
{
  void ImFileDialog_SetTextureCallback(ImFileDialog_CreateTexture on_create, ImFileDialog_DeleteTexture on_delete);
  void ImFileDialog_Open(const char *id, const char *title, const char *filter);
  std::string ImFileDialog_GetResult(const char *id);
}
