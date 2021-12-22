#include "ImFileDialogWrap.h"
#include "ImFileDialog/ImFileDialog.h"

namespace ifd
{
  void ImFileDialog_SetTextureCallback(ImFileDialog_CreateTexture on_create, ImFileDialog_DeleteTexture on_delete)
  {
    ifd::FileDialog::Instance().CreateTexture = on_create;
    ifd::FileDialog::Instance().DeleteTexture = on_delete;
  }

  void ImFileDialog_Open(const char *id, const char *title, const char *filter)
  {
    ifd::FileDialog::Instance().Open(id, title, filter);
  }

  std::string ImFileDialog_GetResult(const char *id)
  {
    if (!ifd::FileDialog::Instance().IsDone(id))
    {
      return {};
    }
    if (!ifd::FileDialog::Instance().HasResult())
    {
      return {};
    }

    auto res = ifd::FileDialog::Instance().GetResult().string();
    ifd::FileDialog::Instance().Close();
    return res;
  }
}
