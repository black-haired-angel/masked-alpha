def create_ui():
    interfaces = []

    # 既存のUI要素を追加
    # 例: interfaces.append((existing_interface, "Existing Label", "existing_id"))

    # Masked Alpha ExtensionのUI要素を追加
    from extensions.masked_alpha.masked_alpha import on_ui_tabs
    interfaces.extend(on_ui_tabs())

    with gr.Blocks() as demo:
        for _interface, label, _ifid in interfaces:
            with gr.TabItem(label):
                _interface.render()

    return demo
