# Mermaid diagram for overall structure and flow

Needs updating to match terms in the app

```mermaid
flowchart LR
    subgraph flow
        direction LR

        midi_event --> input_mapping --> widget --> binding --> system_event

        subgraph config
            direction BT
            device_config
            widget_config
        end
        device_config --> input_mapping
        widget_config --> binding

    end
    subgraph structure
        direction TB
        midi_listener -->|queue| event_handler
        system_listener -->|queue| event_handler
        event_handler -->|call| midi_sender
        event_handler -->|call| system_sender
    end
```
