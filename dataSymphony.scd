// local machine test
n = NetAddr("127.0.0.1", 57120);
n.sendMsg('/d/mx', 2);

// reverb
~revbus = Bus.audio(s,2);
Ndef(\rev, {GVerb.ar(In.ar(~revbus),100, 10)}).play(0,2);

// synth
~mx = {arg amp = 1, rl,bn, out; Synth(\sampleNarcodeStr, [\buf, ~buffers['rabinal'][bn], \amp, amp, \rl, rl, \out, out])};
~india = {arg amp = 1, rl,bn,out; Synth(\sampleNarcodeStr, [\buf, ~buffers['india'][bn], \amp, amp, \rl, rl, \out, out])};
~iran = {arg amp = 1, rl,bn,out; Synth(\sampleNarcodeStr, [\buf, ~buffers['iran'][bn], \amp, amp, \rl, rl, \out, out])};
~indo = {arg amp = 1, rl,bn,out; Synth(\sampleNarcodeStr, [\buf, ~buffers['indonesia'][bn], \amp, amp, \rl, rl, \out, out])};

(
// v1
OSCdef(\mx1, {|msg, time, addr, recvPort|
	// msg.postln;
	~mx.(1,msg[1],1.rrand(36),~revbus);
}, '/d/mx');

OSCdef(\india1, {|msg, time, addr, recvPort|
	// msg.postln;
	~india.(1,msg[1],1.rrand(7),~revbus);
}, '/d/india');

OSCdef(\iran1, {|msg, time, addr, recvPort|
	// msg.postln;
	~iran.(1,msg[1],1.rrand(26),~revbus);
}, '/d/iran');

OSCdef(\indo1, {|msg, time, addr, recvPort|
	// msg.postln;
	~indo.(1,msg[1],1.rrand(18),~revbus);
}, '/d/indo');


// v2
~rl = 1;
~ampv2=1;
OSCdef(\mx, {|msg, time, addr, recvPort|
	msg.postln;
	{
	msg[1].do{
			~mx.(~ampv2,~rl,msg[1].round.clip2(35).asInteger, 0.rrand(1));
		(1/msg[1]).wait;
		};
	}.fork;
}, '/d/mx');

OSCdef(\india, {|msg, time, addr, recvPort|
	msg.postln;
	{
	msg[1].do{
	~india.(~ampv2,~rl,msg[1].round.clip2(7).asInteger,0.rrand(1));
		(1/msg[1]).wait;
		};
	}.fork
}, '/d/india');

OSCdef(\iran, {|msg, time, addr, recvPort|
	msg.postln;
	{
	msg[1].do{
	~iran.(~ampv2,~rl,msg[1].round.clip2(26).asInteger,0.rrand(1));
		(1/msg[1]).wait;
		};
	}.fork;
}, '/d/iran');

OSCdef(\indo, {|msg, time, addr, recvPort|
	msg.postln;
		{
	msg[1].do{
	~indo.(~ampv2*0.5,~rl,msg[1].round.clip2(18).asInteger,0.rrand(1));
		(1/msg[1]).wait;
		}
		}.fork;
}, '/d/indo');
);
