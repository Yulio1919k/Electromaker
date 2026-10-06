from django.core.management.base import BaseCommand

from core.models import Platform, Post, Project

PLATFORMS = [
    ('Adafruit', 'Unique and fun DIY electronics and kits, open source hardware, and the best tutorials on the web!'),
    ('Amazon Alexa', "Alexa is Amazon's cloud-based voice service available on over 100 million devices from Amazon and third-party device manufacturers."),
    ('Android', 'The open-source operating system for mobile devices. With over 2.5 billion active devices worldwide, Android is everywhere.'),
    ('Arduino', "Arduino is the world's leading open-source hardware and software ecosystem. The Company offers a range of software tools, hardware platforms and documentation."),
    ('Balena', 'Balena is a complete set of tools for building, deploying, and managing fleets of connected Linux devices.'),
    ('BeagleBoard', 'Beagleboards are low-cost, fan-less single-board computers based on low-power Texas Instruments processors.'),
    ('Blues', 'The Notecard and Notehub make wireless IoT developer-friendly. Finally.'),
    ('DFRobot', 'DFRobot was founded by a local maker community in 2008, among the first to embrace open-source hardware.'),
    ('Elecrow', 'Elecrow offers open-source hardware, displays and kits for makers and educators.'),
    ('Espressif', 'Espressif makes the ESP32 family of low-cost Wi-Fi and Bluetooth chips popular with makers.'),
    ('Raspberry Pi', 'Raspberry Pi makes low-cost single-board computers and microcontrollers for learning and building.'),
    ('Seeed Studio', 'Seeed Studio provides modular hardware, the XIAO boards and Grove sensors for IoT projects.'),
]
# (titulo, resumen, autor, dificultad, categoria, plataforma)
PROJECTS = [
    ('Native Linux 7.2.4 On Esp32-s3', 'Native Linux 7.2.4 running directly on a single ESP32-S3 N16R8. The project includes WiFi, a shell and a small root filesystem.', 'Paulneja', 'Difficult', 'Software', 'Espressif'),
    ('Murdrum', 'Eight voice MIDI drum sample player for Eurorack, 3U/6HP or 1U/20HP.', 'robmurru', 'Difficult', 'Audio', ''),
    ('Ewatch: An Open Esp32-s3 Smartwatch You Program With Ai', 'A full ESP32-S3 dev board in a watch: 1.69" colour touchscreen, USB-C, WiFi, Bluetooth and a battery.', 'ewan-wills', 'Expert', 'Wearables', 'Espressif'),
    ('Shopcam 2000: A Button That Records The Past', 'A battery ESP32-S3 "That was Awesome" button saves the last sixty seconds from nine cameras.', 'Dan', 'Moderate', 'Camera', 'Espressif'),
    ('Case Study: Esp32-s3 Smart Curtain Automation Controller', 'A European window treatments company came to us with a problem. Their motorized curtains needed one controller.', 'chanchaldada', 'Expert', 'Home Automation', 'Espressif'),
    ('Voice-driven Car', 'This car has 4 wheels, each wheel has tyre and filled with air and petrol', 'ashokr', 'Difficult', 'Robotics', ''),
    ('ESP32 Weather Station', 'Temperature, humidity and pressure on a small display, with readings sent over WiFi.', 'demo', 'Easy', 'IoT', 'Espressif'),
    ('Arduino Line-Following Robot', 'A two-wheel robot that follows a black line using infrared sensors.', 'demo', 'Easy', 'Robotics', 'Arduino'),
    ('Blues Notecard Soil Monitor', 'A cellular soil moisture sensor that reports once an hour from the field.', 'demo', 'Moderate', 'IoT', 'Blues'),
    ('Raspberry Pi Cloud Drive', 'A personal cloud with a Raspberry Pi and an external hard drive, reachable from anywhere.', 'demo', 'Moderate', 'IoT', 'Raspberry Pi'),
]
# (titulo, resumen, autor, tipo, categoria, plataforma, tag)
POSTS = [
    ('Maker Faire Rome 2026: Humanoid Robots, Driverless Cars and 400+ Exhibits', 'Maker Faire Rome returns from 23 to 25 October 2026 with more than 400 exhibits, workshops and talks.', 'Richard Elliot', 'News', 'Events', '', ''),
    ('PicoScope 2205A Guide: Specs, Setup and Practical Projects', 'The PicoScope 2205A is a compact two-channel USB oscilloscope with 25 MHz bandwidth and 8-bit resolution.', 'Richard Elliot', 'News', 'Test & Measurement', '', 'potw'),
    ('Hailo-8 vs Hailo-8L vs Hailo-10H: Which AI Accelerator Should You Buy?', 'Compare Hailo-8, Hailo-8L and Hailo-10H for Raspberry Pi, Frigate, computer vision and generative AI.', 'Richard Elliot', 'Review', 'AI', 'Raspberry Pi', ''),
    ('LattePanda Mu Ultra Launches With Up to 115 TOPS for Local AI', 'LattePanda Mu Ultra launches with Intel Core Ultra 226V/256V options, up to 115 TOPS and x86 support.', 'Richard Elliot', 'News', 'AI', 'DFRobot', ''),
    ('Nordic nRF54L15 Tag: Sensors, Setup, and Channel Sounding', "Explore the nRF54L15 Tag's dual antennas, sensors, SDK setup, and tracker development.", 'Richard Elliot', 'News', 'IoT', '', 'potw'),
    ('ELM11 Feather Explained: Lua, C, and FPGA Programming on One Board', 'Explore ELM11 Feather, a Lua-programmable FPGA board with C drivers and hardware control.', 'Robin Mitchell', 'Review', 'Development Kits', '', 'potw'),
    ('Build a Mini Arcade with Arduino Nano R4', 'The project features a 128x64 OLED display, three control buttons, two piezo speakers, and a 3D printed enclosure.', 'Robin Mitchell', 'Tutorial', 'Projects', 'Arduino', 'educator'),
    ('Nvidia Jetson Lineup Explained from Nano to AGX Orin', 'Robin looks at the full Nvidia Jetson lineup: how each module performs, how much power it draws and where it works best.', 'Robin Mitchell', 'Review', 'AI', '', ''),
    ('Cellular IoT in 2026, Best Dev Kits and Modules Compared', 'Robin compares the Nordic nRF9151 DK, Blues Wireless Notecard, Particle M404 and more, with pros and cons.', 'Robin Mitchell', 'Review', 'IoT', 'Blues', ''),
    ('Top SBC Picks in 2026 for Engineers & Developers', 'A deep dive into performance, connectivity and real-world usability across single board computers.', 'Robin Mitchell', 'Review', 'Single Board Computers', 'Raspberry Pi', ''),
    ('The Electromaker Show Podcast', 'Listen to the Electromaker Show on the go!', 'Electromaker', 'Podcast', 'Podcast', '', 'podcast'),
]

PLATFORMS += [
    ('Digilent Inc', 'Digilent Inc., a National Instruments company, is a leader in the design and manufacture of test and measurement tools.'),
    ('Elephant Robotics', 'Elephant Robotics is a technology firm specializing in the design and production of robotic arms and development kits.'),
    ('Espruino', 'Espruino, Espruino Pico and Puck.js are low-power microcontrollers that run JavaScript.'),
    ('Google', 'Google offers a wide range of tools for you to build high-quality apps as quickly and reliably as possible.'),
    ('Infineon Technologies', 'Our semiconductor and system solutions contribute to a better future, making our world easier, safer and greener.'),
    ('M5Stack', 'We design and manufacture open-source development toolkits, including hardware and programming platforms.'),
    ('Microchip', 'Microchip provides microcontrollers, analog and connectivity solutions for embedded designs.'),
    ('Nordic Semiconductor', 'Nordic makes low-power wireless chips for Bluetooth LE, Thread, Zigbee and cellular IoT.'),
    ('NVIDIA', 'NVIDIA Jetson brings accelerated AI computing to compact edge devices and robots.'),
    ('Particle', 'Particle provides connected hardware, cloud and tools for building IoT products at scale.'),
    ('Pimoroni', 'Pimoroni makes colourful, creative electronics and Raspberry Pi add-ons in Sheffield, UK.'),
    ('SparkFun', 'SparkFun sells open-source breakout boards, sensors and kits with great tutorials.'),
    ('STMicroelectronics', 'ST offers STM32 microcontrollers, sensors and power devices for makers and industry.'),
    ('Texas Instruments', 'TI designs analog and embedded processing chips used in countless maker boards.'),
]
POSTS += [
    ('Raspberry Pi 5 vs Orange Pi 5: Which SBC Wins in 2026?', 'A head-to-head look at CPU, GPU, I/O and software support for two popular single board computers.', 'Robin Mitchell', 'Review', 'Single Board Computers', 'Raspberry Pi', ''),
    ('ESP32-S3 Getting Started: Wi-Fi, BLE and a Tiny Display', 'Set up the toolchain and build a first connected gadget with an ESP32-S3 board.', 'Robin Mitchell', 'Tutorial', 'Projects', 'Espressif', 'educator'),
    ('Seeed Studio XIAO Roundup: Every Board Compared', 'From the XIAO SAMD21 to the nRF54, this guide compares size, wireless options and price.', 'Richard Elliot', 'Review', 'Development Kits', 'Seeed Studio', ''),
    ('Top 5 Oscilloscopes for Makers on a Budget', 'Bandwidth, sample rate and software compared across five bench and USB scopes.', 'Richard Elliot', 'Review', 'Test & Measurement', '', ''),
    ('Zephyr RTOS Explained for Beginners', 'What an RTOS is, why Zephyr is popular and how to blink your first LED.', 'Robin Mitchell', 'Tutorial', 'Software', 'Nordic Semiconductor', 'educator'),
    ('M5Stack Unveils New Modular Dev Kit for Education', 'The new kit stacks sensors and displays without soldering, aimed at classrooms.', 'Richard Elliot', 'News', 'Development Kits', 'M5Stack', ''),
    ('Build a Smart Plant Monitor with Arduino', 'Measure soil moisture and light and get alerts when your plant needs water.', 'Robin Mitchell', 'Tutorial', 'Projects', 'Arduino', ''),
    ('Edge AI on a Budget: Running Vision Models on a Pico', 'Tiny machine-learning models for object detection on a microcontroller.', 'Robin Mitchell', 'Review', 'AI', 'Raspberry Pi', ''),
    ('Electromaker Podcast: The Future of Open Hardware', 'We talk open-source hardware, licensing and how makers can turn projects into products.', 'Electromaker', 'Podcast', 'Podcast', '', 'podcast'),
    ('Product of the Week: Adafruit Feather RP2350', 'A compact Feather board with the RP2350, plenty of flash and a LiPo charger.', 'Richard Elliot', 'News', 'Development Kits', 'Adafruit', 'potw'),
]


PLATFORMS += [
    ('Hailo', 'Hailo builds high-performance AI accelerators that bring neural-network inference to edge devices and Raspberry Pi.'),
    ('Pine64', 'Pine64 designs community-driven, low-cost ARM and RISC-V boards, laptops and phones.'),
    ('PJRC Teensy', 'Teensy boards are fast, breadboard-friendly microcontrollers loved for audio, USB and real-time projects.'),
    ('Sipeed', 'Sipeed makes tiny RISC-V and AI boards such as the Maix and LicheePi series for embedded vision.'),
    ('Luckfox', 'Luckfox offers compact Rockchip-based Linux boards with camera support at very low prices.'),
    ('Orange Pi', 'Orange Pi produces affordable single board computers with strong CPU, NPU and I/O options.'),
]
PROJECTS += [
    ('Pico Synth: A Pocket Wavetable Synthesizer', 'A Raspberry Pi Pico plays 16-voice wavetable sounds through an I2S DAC with a rotary encoder UI.', 'synthlab', 'Moderate', 'Audio', 'Raspberry Pi'),
    ('Smart Plant Watering System', 'Capacitive soil sensors and a small pump keep houseplants alive while you are away, with alerts over WiFi.', 'greenthumb', 'Easy', 'Home Automation', 'Arduino'),
    ('LoRa Mesh Messenger', 'Off-grid text messaging between handheld ESP32 boards using LoRa radios and an e-paper screen.', 'meshmaker', 'Difficult', 'IoT', 'Espressif'),
    ('Desk Robot Arm With Servo Control', 'A 4-axis printed robot arm driven by an Arduino and a web slider interface for pick-and-place tasks.', 'armlab', 'Moderate', 'Robotics', 'Arduino'),
    ('Pocket Oscilloscope From a Pico', 'Turn a Raspberry Pi Pico into a 500 kS/s scope with a small TFT display and trigger controls.', 'scopefan', 'Moderate', 'Test & Measurement', 'Raspberry Pi'),
    ('Wi-Fi Doorbell Camera', 'A tiny ESP32-S3 camera sends a snapshot to your phone whenever the doorbell button is pressed.', 'doorbellman', 'Moderate', 'Camera', 'Espressif'),
    ('E-Paper Calendar Dashboard', 'A 7.5-inch e-paper display shows the weekly calendar, weather and to-do list for weeks on a battery.', 'inkdesign', 'Easy', 'Home Automation', 'Raspberry Pi'),
    ('Gesture-Controlled Lamp', 'Wave your hand to dim or change the colour of an addressable LED lamp using a time-of-flight sensor.', 'lumen', 'Easy', 'Home Automation', 'Seeed Studio'),
    ('BLE Asset Tracker With nRF54', 'A low-power Bluetooth tracker that logs location pings and sleeps for months on a coin cell.', 'trackdev', 'Expert', 'IoT', 'Nordic Semiconductor'),
    ('Jetson Nano Object Detector', 'Real-time person and vehicle detection on a Jetson Nano with a USB camera and a small web dashboard.', 'visionguy', 'Difficult', 'AI', 'NVIDIA'),
    ('Retro Handheld Game Console', 'A 3D-printed handheld that runs classic 8-bit games on an RP2040 with a colour LCD and stereo sound.', 'pixelpete', 'Difficult', 'Software', 'Raspberry Pi'),
    ('Fitness Band With Heart-Rate Sensor', 'A flexible wearable that tracks heart rate and steps and syncs to your phone over Bluetooth LE.', 'bandlab', 'Expert', 'Wearables', 'Nordic Semiconductor'),
    ('Solar-Powered Weather Node', 'A LoRaWAN weather node with a solar panel and supercapacitor that runs all year without batteries.', 'sunny', 'Expert', 'IoT', 'Particle'),
    ('Beginner LED Blinking Board', 'Your first soldering project: a through-hole board with a 555 timer and a row of blinking LEDs.', 'solderfan', 'Easy', 'Projects', ''),
    ('Wi-Fi Smart Plug', 'Switch mains appliances from your phone with an ESP8266 relay board in a safe 3D-printed enclosure.', 'plugin', 'Moderate', 'Home Automation', 'Espressif'),
    ('Hexapod Walker', 'A six-legged robot with 18 servos that walks, turns and climbs small obstacles.', 'bugbot', 'Expert', 'Robotics', 'Arduino'),
    ('USB Audio Interface With Teensy', 'A 2-in 2-out USB audio interface with studio-grade ADCs and a custom aluminium case.', 'audiogeek', 'Difficult', 'Audio', 'PJRC Teensy'),
    ('Pet Feeder With Camera', 'Schedule meals and watch your pet eat from anywhere with an ESP32-CAM and a stepper-driven dispenser.', 'catdad', 'Moderate', 'Camera', 'Espressif'),
    ('Alexa-Controlled Desk Lamp', 'Add voice control to any lamp using an ESP32, a relay and the Alexa smart-home skill.', 'voicehome', 'Easy', 'Home Automation', 'Amazon Alexa'),
    ('Tiny Linux Board With RISC-V', 'A credit-card sized board that boots Linux on a RISC-V SoC with Ethernet, USB and a camera port.', 'riscvfan', 'Expert', 'Single Board Computers', 'Sipeed'),
]
POSTS += [
    ('Raspberry Pi AI HAT+ 2 Review: Local LLMs on a Pi', 'We test the new AI HAT+ with Hailo-10H for chat, vision and speech models running fully offline.', 'Robin Mitchell', 'Review', 'AI', 'Hailo', ''),
    ('Teensy 4.1 Audio Projects You Can Build This Weekend', 'Effects pedals, synths and a USB mixer: five audio builds that make the most of the Teensy Audio Library.', 'Robin Mitchell', 'Tutorial', 'Audio', 'PJRC Teensy', 'educator'),
    ('Pine64 Announces New RISC-V Single Board Computer', 'Pine64 shows an open RISC-V board with 8 GB of RAM, M.2 storage and mainline Linux support.', 'Richard Elliot', 'News', 'Single Board Computers', 'Pine64', ''),
    ('How to Choose a Soldering Iron in 2026', 'Temperature control, tip shapes and power: what to look for in your first or next soldering station.', 'Richard Elliot', 'Review', 'Projects', '', ''),
    ('Home Assistant Meets ESP32: Build a Room Sensor', 'Combine ESPHome, a temperature sensor and a presence radar to build a smart room sensor in an afternoon.', 'Robin Mitchell', 'Tutorial', 'Home Automation', 'Espressif', 'educator'),
    ('Product of the Week: Seeed Studio XIAO ESP32-C6', 'Wi-Fi 6, Bluetooth 5 and Thread in a thumb-sized board that costs less than a coffee.', 'Richard Elliot', 'News', 'Development Kits', 'Seeed Studio', 'potw'),
    ('Wearable Tech Trends: What Makers Are Building in 2026', 'Smart rings, e-textiles and open smartwatches: a look at the hottest wearable projects this year.', 'Robin Mitchell', 'News', 'Wearables', '', ''),
    ('Electromaker Podcast: Is RISC-V Ready for Makers?', 'We discuss RISC-V boards, toolchains and whether now is the time to switch from ARM.', 'Electromaker', 'Podcast', 'Podcast', '', 'podcast'),
    ('Orange Pi 6 Plus First Look', 'An 8-core board with a powerful NPU and dual 2.5G Ethernet: is this the new SBC to beat?', 'Richard Elliot', 'Review', 'Single Board Computers', 'Orange Pi', ''),
    ('Product of the Week: Luckfox Pico Ultra', 'A tiny Linux board with a camera interface and NPU that runs vision models for under thirty dollars.', 'Richard Elliot', 'News', 'AI', 'Luckfox', 'potw'),
    ('Electromaker Educator: Soldering for Absolute Beginners', 'Everything you need to start soldering: tools, safety, technique and your first practice board.', 'Robin Mitchell', 'Tutorial', 'Projects', '', 'educator'),
    ('Robot Arms for Makers: Elephant Robotics MyCobot Hands-On', 'We unbox, program and test a desktop collaborative robot arm and look at what you can build with it.', 'Robin Mitchell', 'Review', 'Robotics', 'Elephant Robotics', ''),
    ('Digilent Analog Discovery 3 vs PicoScope: Which Bench Tool?', 'Two popular USB instruments compared on bandwidth, software and everyday usability for makers.', 'Richard Elliot', 'Review', 'Test & Measurement', 'Digilent Inc', ''),
    ('Open-Source Smart Speaker With Alexa Voice Service', 'Build a smart speaker with a microphone array, a small amplifier and the Alexa Voice Service SDK.', 'Robin Mitchell', 'Tutorial', 'Audio', 'Amazon Alexa', ''),
    ('Electromaker Podcast: Interview With a Maker Faire Organiser', 'What goes into running a Maker Faire and how to exhibit your own project for the first time.', 'Electromaker', 'Podcast', 'Podcast', '', 'podcast'),
]


class Command(BaseCommand):
    help = 'Reinicia y carga plataformas, proyectos y entradas de ejemplo'

    def handle(self, *args, **opts):
        Post.objects.all().delete()
        Project.objects.all().delete()
        Platform.objects.all().delete()
        for name, desc in PLATFORMS:
            Platform.objects.create(name=name, description=desc)
        plat = {p.name: p for p in Platform.objects.all()}
        for t, s, a, d, c, p in reversed(PROJECTS):
            Project.objects.create(title=t, summary=s, author=a, difficulty=d, category=c, platform=plat.get(p))
        for t, s, a, k, c, p, g in reversed(POSTS):
            Post.objects.create(title=t, summary=s, author=a, kind=k, category=c, platform=plat.get(p), tag=g)
        self.stdout.write('Datos de ejemplo cargados.')
