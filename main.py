
import re
import json

import aiohttp


def read_lines(path):
    with open(path) as file:
        for line in file:
            yield line.rstrip('\n')


def write_lines(path, lines):
    with open(path, 'w') as file:
        for line in lines:
            file.write(line + '\n')


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)


def format_jsonl(items):
    for item in items:
        yield json.dumps(item, ensure_ascii=False)


def item_prompt(item):
    prompt = item['instruction']
    input = item.get('input')
    if input:
        prompt += '\nДано: ' + input
    return prompt


########
#
#   YAGPT
#
#####


async def yagpt_call(prompt):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://uniproxy.alice.ya.ru/uni.ws', timeout=5) as ws:

            data = '{"event":{"header":{"namespace":"System","name":"SynchronizeState","messageId":"87864bdb-3225-431a-8c6e-64d789b5849f","seqNumber":1},"payload":{"auth_token":"effd5a3f-fd42-4a18-83a1-61766a6d0924","uuid":"00000000000001575856741644688509","vins":{"application":{"app_id":"ru.yandex.webdesktop","platform":"macos"}}}}}'
            await ws.send_str(data)

            data = '{"event":{"header":{"namespace":"Vins","name":"TextInput","messageId":"a147db36-c60d-49f3-9755-89c2b5cc7cd8","seqNumber":2},"payload":{"application":{"app_id":"ru.yandex.webdesktop","app_version":"2023-07-03-317","platform":"macos","os_version":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/605.1.15 (khtml, like gecko) version/16.5.1 safari/605.1.15","uuid":"00000000000001575856741644688509","lang":"ru-RU","client_time":"20230705T122852","timezone":"Europe/Moscow","timestamp":"1688560132"},"header":{"prev_req_id":null,"sequence_number":null,"request_id":"9fffa07d-6563-43d9-b0b3-286e1cc86998","dialog_id":null},"request":{"event":{"name":"@@mm_semantic_frame","payload":{"typed_semantic_frame":{"onboarding_get_greetings_semantic_frame":{}},"analytics":{"purpose":"get_greetings","origin":"ThisClient"}},"type":"server_action"},"voice_session":false,"experiments":["set_symbols_per_second=200","search_use_cloud_ui","weather_use_cloud_ui","enable_open_link_and_cloud_ui","hw_onboarding_enable_greetings","remove_feedback_suggests","shopping_list","enable_external_skills_for_webdesktop_and_webtouch","send_show_view_directive_on_supports_show_view_layer_content_interface","use_app_host_pure_Dialogovo_scenario"],"additional_options":{"bass_options":{"screen_scale_factor":2},"supported_features":["open_link","server_action","cloud_ui","cloud_first_screen_div","cloud_ui_filling","show_promo","show_view_layer_content","reminders_and_todos","div2_cards","print_text_in_message_view","supports_print_text_in_message_view"],"unsupported_features":["player_pause_directive"]},"location":{"lat":55.755863,"lon":37.6177}},"format":"audio/ogg;codecs=opus","mime":"audio/x-pcm;bit=16;rate=16000","topic":"desktopgeneral"}}}'
            await ws.send_str(data)
            await ws.receive()

            data = '{"event":{"header":{"namespace":"Vins","name":"TextInput","messageId":"eb146871-beab-4e23-9d21-9f7b4a107852","seqNumber":3},"payload":{"application":{"app_id":"ru.yandex.webdesktop","app_version":"2023-07-03-317","platform":"macos","os_version":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/605.1.15 (khtml, like gecko) version/16.5.1 safari/605.1.15","uuid":"00000000000001575856741644688509","lang":"ru-RU","client_time":"20230705T122905","timezone":"Europe/Moscow","timestamp":"1688560145"},"header":{"prev_req_id":"9fffa07d-6563-43d9-b0b3-286e1cc86998","sequence_number":null,"request_id":"708c908e-c08b-452c-a76d-b98e59d30558","dialog_id":null},"request":{"event":{"type":"suggested_input","text":"Запусти навык «Давай придумаем»"},"voice_session":false,"experiments":["set_symbols_per_second=200","search_use_cloud_ui","weather_use_cloud_ui","enable_open_link_and_cloud_ui","hw_onboarding_enable_greetings","remove_feedback_suggests","shopping_list","enable_external_skills_for_webdesktop_and_webtouch","send_show_view_directive_on_supports_show_view_layer_content_interface","use_app_host_pure_Dialogovo_scenario"],"additional_options":{"bass_options":{"screen_scale_factor":2},"supported_features":["open_link","server_action","cloud_ui","cloud_first_screen_div","cloud_ui_filling","show_promo","show_view_layer_content","reminders_and_todos","div2_cards","print_text_in_message_view","supports_print_text_in_message_view"],"unsupported_features":["player_pause_directive"]},"location":{"lat":55.755863,"lon":37.6177}},"format":"audio/ogg;codecs=opus","mime":"audio/x-pcm;bit=16;rate=16000","topic":"desktopgeneral"}}}'
            await ws.send_str(data)
            message = await ws.receive()
            assert 'Запускаю навык «Давай придумаем»' in message.data, message.data

            data = '{"event":{"header":{"namespace":"Vins","name":"TextInput","messageId":"76402cd4-514a-4ad0-9b9c-7a502257ede1","seqNumber":4},"payload":{"application":{"app_id":"ru.yandex.webdesktop","app_version":"2023-07-03-317","platform":"macos","os_version":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/605.1.15 (khtml, like gecko) version/16.5.1 safari/605.1.15","uuid":"00000000000001575856741644688509","lang":"ru-RU","client_time":"20230705T122908","timezone":"Europe/Moscow","timestamp":"1688560148"},"header":{"prev_req_id":"708c908e-c08b-452c-a76d-b98e59d30558","sequence_number":null,"request_id":"4642bc9d-c4fc-4286-a4a4-5d435039729b","dialog_id":"b7c42cab-db61-46ba-871a-b10a6ecf3e0d"},"request":{"event":{"name":"new_dialog_session","payload":{"should_be_silent":true,"request":"","@request_id":"708c908e-c08b-452c-a76d-b98e59d30558","original_utterance":"","source":"undetected","@scenario_name":"Dialogovo","dialog_id":"b7c42cab-db61-46ba-871a-b10a6ecf3e0d"},"ignore_answer":false,"type":"server_action"},"voice_session":false,"experiments":["set_symbols_per_second=200","search_use_cloud_ui","weather_use_cloud_ui","enable_open_link_and_cloud_ui","hw_onboarding_enable_greetings","remove_feedback_suggests","shopping_list","enable_external_skills_for_webdesktop_and_webtouch","send_show_view_directive_on_supports_show_view_layer_content_interface","use_app_host_pure_Dialogovo_scenario"],"additional_options":{"bass_options":{"screen_scale_factor":2},"supported_features":["open_link","server_action","cloud_ui","cloud_first_screen_div","cloud_ui_filling","show_promo","show_view_layer_content","reminders_and_todos","div2_cards","print_text_in_message_view","supports_print_text_in_message_view"],"unsupported_features":["player_pause_directive"]},"location":{"lat":55.755863,"lon":37.6177}},"format":"audio/ogg;codecs=opus","mime":"audio/x-pcm;bit=16;rate=16000","topic":"desktopgeneral"}}}'
            await ws.send_str(data)
            message = await ws.receive()
            assert 'В этом режиме я помогаю придумывать — идеи, тексты на разные темы и многое другое' in message.data, message.data
    
            for step in range(5):
                if step == 0:
                    data = '{"event":{"header":{"namespace":"Vins","name":"TextInput","messageId":"7499a1ef-9c4c-4097-8872-6f9bace8cba4","seqNumber":7},"payload":{"application":{"app_id":"ru.yandex.webdesktop","app_version":"2023-07-04-318","platform":"macos","os_version":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/605.1.15 (khtml, like gecko) version/16.5.1 safari/605.1.15","uuid":"00000000000009431933201688623980","lang":"ru-RU","client_time":"20230706T062211","timezone":"Europe/Moscow","timestamp":"1688624531"},"header":{"prev_req_id":"4642bc9d-c4fc-4286-a4a4-5d435039729b","sequence_number":null,"request_id":"8d524be4-4540-4492-894d-b37c0191e69d","dialog_id":"b7c42cab-db61-46ba-871a-b10a6ecf3e0d"},"request":{"event":{"type":"suggested_input","text":"Как уговорить мужа купить кота"},"voice_session":false,"experiments":["set_symbols_per_second=200","search_use_cloud_ui","weather_use_cloud_ui","enable_open_link_and_cloud_ui","hw_onboarding_enable_greetings","remove_feedback_suggests","shopping_list","enable_external_skills_for_webdesktop_and_webtouch","send_show_view_directive_on_supports_show_view_layer_content_interface","use_app_host_pure_Dialogovo_scenario"],"additional_options":{"bass_options":{"screen_scale_factor":2},"supported_features":["open_link","server_action","cloud_ui","cloud_first_screen_div","cloud_ui_filling","show_promo","show_view_layer_content","reminders_and_todos","div2_cards","print_text_in_message_view","supports_print_text_in_message_view"],"unsupported_features":["player_pause_directive"]},"location":{"lat":55.755863,"lon":37.6177}},"format":"audio/ogg;codecs=opus","mime":"audio/x-pcm;bit=16;rate=16000","topic":"desktopgeneral"}}}'
                    data = data.replace('"Как уговорить мужа купить кота"', json.dumps(prompt))
                else:
                    data = '{"event":{"header":{"namespace":"Vins","name":"TextInput","messageId":"2aa61cfb-17b8-4ffd-982c-45593a14faaa","seqNumber":8},"payload":{"application":{"app_id":"ru.yandex.webdesktop","app_version":"2023-07-04-318","platform":"macos","os_version":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/605.1.15 (khtml, like gecko) version/16.5.1 safari/605.1.15","uuid":"00000000000009431933201688623980","lang":"ru-RU","client_time":"20230706T062213","timezone":"Europe/Moscow","timestamp":"1688624533"},"header":{"prev_req_id":"8d524be4-4540-4492-894d-b37c0191e69d","sequence_number":null,"request_id":"a97f4954-b291-4e0b-ab2d-bb8e8057d414","dialog_id":"b7c42cab-db61-46ba-871a-b10a6ecf3e0d"},"request":{"event":{"type":"server_action","name":"@@mm_stack_engine_get_next","payload":{"@request_id":"8d524be4-4540-4492-894d-b37c0191e69d","stack_session_id":"8d524be4-4540-4492-894d-b37c0191e69d","@recovery_params":{},"@scenario_name":"Dialogovo","stack_product_scenario_name":"dialogovo"}},"voice_session":false,"experiments":["set_symbols_per_second=200","search_use_cloud_ui","weather_use_cloud_ui","enable_open_link_and_cloud_ui","hw_onboarding_enable_greetings","remove_feedback_suggests","shopping_list","enable_external_skills_for_webdesktop_and_webtouch","send_show_view_directive_on_supports_show_view_layer_content_interface","use_app_host_pure_Dialogovo_scenario"],"additional_options":{"bass_options":{"screen_scale_factor":2},"supported_features":["open_link","server_action","cloud_ui","cloud_first_screen_div","cloud_ui_filling","show_promo","show_view_layer_content","reminders_and_todos","div2_cards","print_text_in_message_view","supports_print_text_in_message_view"],"unsupported_features":["player_pause_directive"]},"location":{"lat":55.755863,"lon":37.6177}},"format":"audio/ogg;codecs=opus","mime":"audio/x-pcm;bit=16;rate=16000","topic":"desktopgeneral"}}}'

                await ws.send_str(data)
                message = await ws.receive(timeout=10)
                match = re.search(r'"is_end":(true|false),"prefetch_after_ms":\d+,"text":(".*"),"should_rewrite":(true|false)', message.data)
                assert match, message.data
                is_end, text, should_rewrite = [json.loads(_) for _ in  match.groups()]
                yield text
                
                if is_end:
                    break
