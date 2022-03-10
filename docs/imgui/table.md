# Table

```py
    flags = (
        ImGui.ImGuiTableFlags_.BordersV
        | ImGui.ImGuiTableFlags_.BordersOuterH
        | ImGui.ImGuiTableFlags_.Resizable
        | ImGui.ImGuiTableFlags_.RowBg
        | ImGui.ImGuiTableFlags_.NoBordersInBody
    )

    if ImGui.BeginTable("tiles", 4, flags):
        # header
        # ImGui.TableSetupScrollFreeze(0, 1); // Make top row always visible
        ImGui.TableSetupColumn('index')
        ImGui.TableSetupColumn('x')
        ImGui.TableSetupColumn('y')
        ImGui.TableSetupColumn('z')
        ImGui.TableHeadersRow()
    
        # body
        for i, p in enumerate(self.positions):
            ImGui.TableNextRow()
            # index
            ImGui.TableNextColumn()
            ImGui.TextUnformatted(f'{i}')
            #
            ImGui.TableNextColumn()
            ImGui.TextUnformatted(f'{p.x:.2f}')
            ImGui.TableNextColumn()
            ImGui.TextUnformatted(f'{p.y:.2f}')
            ImGui.TableNextColumn()
            ImGui.TextUnformatted(f'{p.z:.2f}')

        ImGui.EndTable()
```
